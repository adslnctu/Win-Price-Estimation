import os, sys
import bz2
from bson import json_util
import json
import datetime
from operator import itemgetter
sys.path.append('../lib/ftrlProximal/')
from ftrlProximal import FTRLProximal
sys.path.append('../lib/dbFeatureHasher/')
from dbFeatureHasher import DBFeatureHasher
import pickle

def run(season, date):
	if season==2:
		impFilename="../ipinyou.contest.dataset/training2nd/imp."+date.strftime("%Y%m%d")+".txt.bz2"
		clkFilename="../ipinyou.contest.dataset/training2nd/clk."+date.strftime("%Y%m%d")+".txt.bz2"
	if season==3:
		impFilename="../ipinyou.contest.dataset/training3rd/imp."+date.strftime("%Y%m%d")+".txt.bz2"
		clkFilename="../ipinyou.contest.dataset/training3rd/clk."+date.strftime("%Y%m%d")+".txt.bz2"
	bzFile=bz2.BZ2File(impFilename)
	bid_idList=list()
	sessionList=list()
	for line in bzFile:
		ss=line.replace("\n", "").split("\t")
		x=dict()
		bid_id=str(ss[0])
		x['ip']=str(ss[5])	
		x['region']=str(ss[6])
		x['city']=str(ss[7])
		x['ad_exchange']=str(ss[8])
		x['domain']=str(ss[9])
		x['url']=str(ss[10])
		x['ad_slot_id']=str(ss[12])
		x['ad_slot_width']=str(ss[13])
		x['ad_slot_height']=str(ss[14])
		x['ad_slot_visibility']=ss[15]
		x['ad_slot_format']=str(ss[16])
		x['creative_id']=str(ss[18])
		time1 = datetime.datetime.strptime(ss[1], "%Y%m%d%H%M%S%f")
		x['weekday']=str(time1.weekday())
		x['hour']=str(time1.hour)	
		x['advertiser_id']=str(ss[22])
		user_tag_list=str(ss[23]).split(',')
                for user_tag in user_tag_list:
                        x['user_tag: '+user_tag]=True
                click = False  #click or not
		win_price = float(ss[20])  # paying_price
		bid_price = float(ss[19])
		#x['log_type']=str(ss[2])
		#x['ipinyou_id']=str(ss[3])
		#x['user_agent']=str(ss[4])
		#x['anonymous_url_id']=str(ss[11])
		#x['ad_slot_floor_price']=float(ss[17])
		#x['key_page_url']=str(ss[21])
		
		bid_idList.append(bid_id)
		sessionList.append({"timestamp":time1, "x": x, "click": click, "win_price": win_price, "bid_price": bid_price})
	bzFile.close()
	bzFile=bz2.BZ2File(clkFilename)
	#insert click data form xxx.click file
	for line in bzFile:
		ss=line.replace("\n", "").split("\t")
		bid_id=str(ss[0])
		sessionList[bid_idList.index(bid_id)]["click"]=True
	bzFile.close()


	#sort sessionList by timestamp
	sort_sessionList = list()
	for session in sorted(sessionList, key=lambda x: x['timestamp']):
		sort_sessionList.append(session)
	del sessionList
	
	#predict CTR by Ftrl_proximal
	ftrlproximal=FTRLProximal(alpha=0.1, beta=1, lambda1=0.1, lambda2=0.1, n_features=pow(2, 20))
	CTRsessionList = ftrlproximal.onlineRun(db=sort_sessionList, updateTimedelta=datetime.timedelta(minutes=10))		
	del sort_sessionList

	#generate simulated data(if bidding_price*ratio>paying_price  => win)
	ratioList = [0.167, 0.333, 0.5, 0.667, 0.833]
	simulatedNameList = ["simulated_1_6", "simulated_2_6", "simulated_3_6", "simulated_4_6", "simulated_5_6"]
	dbFeatureHasher=DBFeatureHasher(n_features= pow(2, 20))
	for i in xrange(0, len(ratioList)):	
		print "ratio:", ratioList[i]
		train_data = list()
		trainX = list()
		trainY = list()
		label_list = list()
		train_bidprice = list()
		for j in xrange(0, len(CTRsessionList)):
			if CTRsessionList[j]['win_price']!= 0:
				if CTRsessionList[j]['bid_price']*ratioList[i]>CTRsessionList[j]['win_price']:
					CTRsessionList[j]['label'] = "win"
				elif CTRsessionList[j]['bid_price']*ratioList[i]<=CTRsessionList[j]['win_price']:
					CTRsessionList[j]['label'] = "lose"
				X, Y = dbFeatureHasher.transformToNumeric(CTRsessionList[j]['x'], CTRsessionList[j]['win_price'])
				train_data.append(X)
				trainY.append(Y)
				train_bidprice.append(CTRsessionList[j]['bid_price'])
				label_list.append(CTRsessionList[j]['label'])

		trainX = dbFeatureHasher.featureHashing(train_data)
		del train_data
		if season==2:
			filename = "./log/season2/"+simulatedNameList[i]+"/"+date.strftime("%Y-%m-%d")+".pickle"
		else:
			filename = "./log/season3/"+simulatedNameList[i]+"/"+date.strftime("%Y-%m-%d")+".pickle"
		pickle.dump((trainX, trainY, train_bidprice, label_list), open(filename, "wb"))



def main():
	season2List = [6, 7, 8, 9, 10, 11, 12]
	season3List = [19, 20, 21, 22, 23, 24, 25, 26, 27]
	
	for i in xrange(0, len(season2List)):
		print "process 2013-06-%02d"%(season2List[i],)
                run(2, datetime.date(year=2013, month=6, day=season2List[i]))
	
	for i in xrange(0, len(season3List)):
		print "process 2013-10-%02d"%(season3List[i],)
		run(3, datetime.date(year=2013, month=10, day=season3List[i]))	
	
if __name__=="__main__":
	sys.stdout=os.fdopen(sys.stdout.fileno(), 'w', 0)
	main()
