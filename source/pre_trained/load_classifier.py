import sys

from sklearn.cross_validation import KFold as kfold
from sklearn.ensemble import RandomForestClassifier as rfc

from sklearn.externals import joblib

import numpy as np

if __name__== "__main__":


	test_data = np.loadtxt(sys.argv[1],delimiter =',')
	test_label = np.loadtxt(sys.argv[2],delimiter=',')

	est = joblib.load(sys.argv[3])
	total_count = 0
	correct_count = 0
	for index, value in enumerate(list(est.predict(test_data))):
				total_count += 1
				if int(value) == test_label[index]:
					correct_count += 1 
	print "The accuracy for the loaded model: ", correct_count / (total_count * 1.0)

