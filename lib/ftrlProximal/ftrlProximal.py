import sys, os
import random
from datetime import datetime
import numpy as np
import json
from ftrlProximalProxy import FTRLProximalProxy
sys.path.append('../lib/dbFeatureHasher/')
from dbFeatureHasher import DBFeatureHasher


class FTRLProximal():
	def __init__(self, alpha, beta, lambda1, lambda2, n_features):
		self.ftrlProximalProxy=FTRLProximalProxy(alpha=alpha, beta=beta, lambda1=lambda1, lambda2=lambda2, n_features=n_features)
		self.dbFeatureHasher=DBFeatureHasher(n_features=n_features)
	def onlineRun(self, db, updateTimedelta):
		lastUpdateTime=datetime.min
		
		for i in xrange(0, len(db)):
			x = db[i]['x']
			y = db[i]['click']
			currentTime = db[i]['timestamp']
			X, Y=self.dbFeatureHasher.hash(x, y) 
			p=self.ftrlProximalProxy.predict(X)
			db[i]['x'].update({'pCTR':float(p)})
			self.ftrlProximalProxy.appendToUnupdatedList(X, Y)
			if currentTime-lastUpdateTime>updateTimedelta:
				self.ftrlProximalProxy.update()
				lastUpdateTime=currentTime
				print currentTime

		return db
		
