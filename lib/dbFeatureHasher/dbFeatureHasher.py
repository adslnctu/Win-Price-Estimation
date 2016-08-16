from sklearn.feature_extraction import FeatureHasher
import scipy.sparse as sparse
import numpy as np
import math
class DBFeatureHasher():
	def __init__(self, n_features):
		self.hasher=FeatureHasher(n_features=n_features, input_type="dict")
	def hash(self, x, y):
		newx=dict()
		for key in x.keys():
			value=x[key]
			if type(value)==float or type(value)==int:
				newx[str(key)]=value
			else:
				newx[str(key)+"_"+str(value)]=1
		X=self.hasher.fit_transform([newx])
		Y=int(y)
		return X, Y
	def transformToNumeric(self, x, y):
                newx=dict()
                for key in x.keys():
                        value=x[key]
                        if type(value)==float or type(value)==int:
                                newx[str(key)]=value
                        else:
                                newx[str(key)+"_"+str(value)]=1
                X=newx
                Y=float(y)
                return X, Y
        def featureHashing(self, x):
                X=self.hasher.transform(x)
                return X
	
