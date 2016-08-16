import sys, os
import datetime
import numpy as np
import pickle
import time
from scipy.special import polygamma, gammainc, gammaincc
from math import log, exp, gamma
from mpmath import fp, hyper
from sklearn.metrics import mean_squared_error
from sklearn import linear_model

def LoadData(filename):
        DataX, DataY, DataP, DataLabel = pickle.load(open(filename, "rb"))
	return DataX, DataY, DataP, DataLabel, len(DataY)

def pickleEM(a, b, iterations, thetaName, Trainday, eta1, eta2):
	filename = "./Log/Day"+str(int(Trainday))+"/"+Trainday+"_EM_iteration_"+str(iterations)+"_"+thetaName+"_"+str(eta1)+"_"+str(eta2)+".log"
	pickle.dump((a, b), open(filename, "wb"))

def EM_censored_gamma(thetaName, Trainday, iterations, eta1, eta2, trainY, trainP, trainLabel, n):	
	#initialize of theta
	meanTheta = 0
	winCount = 0
	for i in xrange(0, n):
		if trainLabel[i]=="win":
			meanTheta += trainY[i]
			winCount +=1
	b = 1.0*meanTheta/winCount

	#initialize the alpha
	a = np.array([1.0]*n)
	for i in xrange(0, n):
		if trainLabel[i]=="win":
			a[i] = 1.0*trainY[i]/b
		if trainLabel[i]=="lose":
			a[i] = 1.0*trainP[i]/b
	print "================================================================================"
	print thetaName+"_"+str(eta1)+ "_"+str(eta2)
    	for i in xrange(0, iterations):
        	print "iterations:", i+1
		theta = b
        	for j in xrange(0, n):
			alpha = a[j]
			if trainLabel[j]=="win":
                		a[j] += eta1*(-polygamma(0, alpha)-log(theta)+log(trainY[j]))/n
                		b += eta2*(-1.0*alpha/theta+1.0*trainY[j]/pow(theta,2))/n
               			
            		if trainLabel[j]=="lose":
                		p_theta = 1.0*trainP[j]/theta
                		lowergamma = gammainc(alpha, p_theta)*gamma(alpha)
                		uppergamma = gammaincc(alpha, p_theta)*gamma(alpha)
                		a[j] += 1.0*eta1*(lowergamma*(polygamma(0, alpha)-log(p_theta))+1.0*pow(p_theta, alpha)*hyper([alpha,alpha],[alpha+1,alpha+1], -p_theta)/pow(alpha, 2))/uppergamma/n
    				b += 1.0*eta2*pow(p_theta, alpha)*exp(-p_theta)/(uppergamma*theta*n)
		if i==9 or i==49 or i==99:
			pickleEM(a, b, str(i+1), thetaName, Trainday, eta1, eta2)

def linear_train(thetaName, Trainday, eta1, eta2, trainX, trainY, testX, testY, f):
	iterationList = [10, 50, 100]
	for i in iterationList:
                filename = "./Log/Day"+str(int(Trainday))+"/"+Trainday+"_EM_iteration_"+str(i)+"_"+thetaName+"_"+str(eta1)+"_"+str(eta2)+".log"
		a, b = pickle.load(open(filename, "rb"))
		logY = list()
		for j in xrange(0, len(a)):
			logY.append(log(a[j])+log(b))
		alphaList = [pow(10, -2), pow(10, -1), 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, pow(10, 2), 200, 300, 400, 500, 600, 700, 800, 900, pow(10, 3), 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, pow(10, 4), pow(10, 5)]
        	f.write("Training iteraion"+str(i)+"....... \n")
		for a in alphaList:
        	        clf = linear_model.Ridge (alpha = a)
        	        clf.fit (trainX, logY)

        	        Y = clf.predict(trainX)
        	        predictY = [exp(Y[i]) for i in range(len(Y))]
        	        mse1 = mean_squared_error(trainY, predictY)

        	        Y = clf.predict(testX)
        	        predictY = [exp(Y[i]) for i in range(len(Y))]
        	        mse2 = mean_squared_error(testY, predictY)
			wfile = "\tRidge alpha: "+ str(a)+ "\tvalidation_mse: "+str(mse1)+"\tTesting_mse: "+str(mse2)+"\n"
        	        f.write(wfile)
		f.write("--------------------------------------------------------------------------- \n")

def main():
	trainList = ["06", "07", "08", "09", "10", "11"]
	testList  = ["07", "08", "09", "10", "11", "12"]
	iterations = 100
	eta1List = [pow(10, 1), pow(10, 0), pow(10, -1)]
        eta2List = [pow(10, 2), pow(10, 1), pow(10, 0)]
	thetaName = "meanOfwin"
	for i in xrange(0, len(trainList)):
		#import training data
		trainName = "../../../../log/season2/simulated_5_6/2013-06-"+trainList[i]+".pickle"
		trainX, trainY, trainP, trainLabel, n = LoadData(trainName)

		#import testing data
		testName = "../../../../log/season2/simulated_5_6/2013-06-"+testList[i]+".pickle"
		testX, testY, testingB, testlabel, testn = LoadData(testName)

		ofile = "./Log/mseLog/"+str(int(trainList[i]))+"_RidgeWin.log"
		f = open(ofile, "a")
		f.write("Loading Data Done... \n")
		
		for j in xrange(0, len(eta1List)):
			for k in xrange(0, len(eta2List)):
				start = time.time()
				EM_censored_gamma(thetaName, trainList[i], iterations, eta1List[j], eta2List[k], trainY, trainP, trainLabel, n)	
				print "EM execute time:", time.time()-start

		for j in xrange(0, len(eta1List)):
                        for k in xrange(0, len(eta2List)):
				f.write(thetaName+"_"+str(eta1List[j])+ "_"+str(eta2List[k]))
				f.write("\n")
				linear_train(thetaName, trainList[i], eta1List[j], eta2List[k], trainX, trainY, testX, testY, f)		
		

if __name__=='__main__':
        sys.stdout=os.fdopen(sys.stdout.fileno(), 'w', 0)
        main()

