from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn import decomposition
f = open("features_normalized.txt")
data = []
for line in f:
	line = line.strip()
	data1 = line.split(",")
	data1 = [float(i) for i in data1]
	data1 = np.array(data1)
	data.append(data1)
#data = np.array(data)
labels = []
f.close()
f = open("label")
for line in f:
	line = line.strip()
	labels.append(line)
f.close()
overall_s = 0
for i in range(0,len(data),len(data)/10):
	#labels = np.array(labels)
	train_data = data[0:i] + data[i+len(data)/10:]
	test_data = data[i:i+len(data)/10]
	train_label = labels[0:i] + labels[i+len(data)/10:]
	test_label = labels[i:i+len(data)/10]
	test_label = np.array(test_label)
	train_label = np.array(train_label)
	train_data = np.array(train_data)
	test_data = np.array(test_data)
	#train_data = np.reshape(train_data, (17000,100))
	#test_data = np.reshape(test_data,(len(test_data),100))

	clf = clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(20,2), random_state=1)
	y_pred = clf.fit(train_data,train_label).predict(test_data)
	#pickle.dump( y_pred, open( "out	.p", "wb" ) )
	count = 0
	for i in range(0,len(y_pred)):
		if y_pred[i] == test_label[i]:
			count+=1
	print (float(count)/len(y_pred))*100
	overall_s += (float(count)/len(y_pred))*100
print "overall accuracy is ", overall_s/10