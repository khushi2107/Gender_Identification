import sys

from sklearn.cross_validation import KFold as kfold
from sklearn.ensemble import RandomForestClassifier as rfc


import numpy as np


if __name__== "__main__":

	data = np.loadtxt(sys.argv[1],delimiter =',')
	label = np.loadtxt(sys.argv[2],delimiter=',')

	length_of_data = len(data)
	trees_list = [50,100,300,500] 
	
	print "The accuracies for different number of trees for RandomForestClassifier: "
	for i in trees_list:

		est = rfc(n_estimators=i)

		kf = kfold(length_of_data, n_folds = 10)
		total_count = 0
		for train_index, test_index in kf:
			
			train_data, test_data = data[train_index], data[test_index]
			train_label, test_label = label[train_index], label[test_index]
			est.fit(train_data, train_label)

			partition_count = 0
			for index, value in enumerate(list(est.predict(test_data))):
					if int(value) == test_label[index]:
						partition_count += 1
			#print partition_count
			total_count += partition_count

		print i, ",", (total_count / (length_of_data*1.0))*100
	