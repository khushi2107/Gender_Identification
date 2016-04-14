import sys

from sklearn.cross_validation import KFold as kfold
from sklearn.ensemble import ExtraTreesClassifier as rfc


import numpy as np
from sklearn.externals import joblib


if __name__== "__main__":

	train_data = np.loadtxt(sys.argv[1],delimiter =',')
	train_label = np.loadtxt(sys.argv[2],delimiter=',')
	trees_list = [500]

	for i in trees_list:

		est = rfc(n_estimators=i)
		est.fit(train_data, train_label)
		filename = "extra_tree" + str(i) + ".pkl"
		joblib.dump(est, filename)
