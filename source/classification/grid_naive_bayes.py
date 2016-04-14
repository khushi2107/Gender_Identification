import sys

from sklearn.cross_validation import KFold as kfold
from sklearn.naive_bayes import GaussianNB 
from sklearn.naive_bayes import BernoulliNB

#import pandas as pd
import numpy as np


if __name__== "__main__":
	
	#data = pd.read_csv(sys.argv[1],header=None)
	#label = pd.read_csv(sys.argv[2],header=None)

	data = np.loadtxt(sys.argv[1],delimiter =',')
	label = np.loadtxt(sys.argv[2],delimiter=',')

	length_of_data = len(data)
	#gnb = GaussianNB()
	gnb = BernoulliNB()
	

	kf = kfold(length_of_data, n_folds = 10)
	total_count = 0

	for train_index, test_index in kf:
		
			train_data, test_data = data[train_index], data[test_index]
			train_label, test_label = label[train_index], label[test_index]
			gnb.fit(train_data, train_label)

			partition_count = 0
			for index, value in enumerate(list(gnb.predict(test_data))):
				if int(value) == test_label[index]:
					partition_count += 1
			print partition_count
			total_count += partition_count

	print "The accuracies for the naive_bayes is : ", (total_count / (length_of_data*1.0)) * 100

