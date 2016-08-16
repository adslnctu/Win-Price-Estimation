import pickle
import sys, os
import math
import scipy.sparse as sparse
import itertools
from multiprocessing import Pool 
import numpy as np
import random
from sklearn.metrics import roc_curve, auc
def sigmoid(a):
	return 1.0/(1+math.pow(math.e, -a))
class FTRLProximalProxy:
	def __init__(self, alpha, beta, lambda1, lambda2, n_features):
		self.alpha=alpha
		self.beta=beta
		self.lambda1=lambda1
		self.lambda2=lambda2
		self.d=n_features
		self.zList=[0.0]*self.d
		self.nList=[0.0]*self.d
		self.unupdatedXList=list()
		self.unupdatedYList=list()
	def getw(self, i):
		zi=self.zList[i]
		ni=self.nList[i]
		if abs(zi)<=self.lambda1:
			wi=0
		else:
			sign=int(zi>0)
			wi=-1/((self.beta+math.sqrt(ni))/self.alpha+self.lambda2)*(zi-sign*self.lambda1)
		return wi
	def predict(self, X):
		cX=X.tocoo()
		a=0
		for i, xi in itertools.izip(cX.col, cX.data):
			wi=self.getw(i)
			a+=wi*xi
		p=sigmoid(a)
		return p
	def appendToUnupdatedList(self, X, Y):
		self.unupdatedXList.append(X)
		self.unupdatedYList.append(Y)
	def update(self):
		for X, y in zip(self.unupdatedXList, self.unupdatedYList):
			p=self.predict(X)
			cX=X.tocoo()
			for i, xi in itertools.izip(cX.col, cX.data):
				zi=self.zList[i]
				ni=self.nList[i]
				wi=self.getw(i)
				gi=(p-y)*xi
				sigmai=1.0/self.alpha*(math.sqrt(ni+math.pow(gi, 2))-math.sqrt(ni))
				zi=zi+gi-sigmai*wi
				ni=ni+math.pow(gi, 2)
				self.zList[i]=zi
				self.nList[i]=ni
		self.unupdatedXList=list()
		self.unupdatedYList=list()
