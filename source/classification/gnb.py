from sklearn.naive_bayes import GaussianNB
import numpy as np
import pickle
f = open("features_normalized.txt")
data = []
for line in f:
	line = line.strip()
	data1 = line.split(",")
	data1 = [float(i) for i in data1]
	data1 = np.array(data1)
	data.append(data1)
data = np.array(data)
labels = []
f.close()
f = open("label")
for line in f:
	line = line.strip()
	labels.append(line)
f.close()
labels = np.array(labels)
train_data = data[0:17000]
test_data = data[17000:]
train_label = labels[0:17000]
test_label = labels[17000:]
#train_data = np.reshape(train_data, (17000,100))
#test_data = np.reshape(test_data,(len(test_data),100))
gnb = GaussianNB()
y_pred = gnb.fit(train_data, train_label).predict(test_data)
#pickle.dump( y_pred, open( "out	.p", "wb" ) )
print y_pred
print test_label
count = 0
for i in range(0,len(y_pred)):
	if y_pred[i] == test_label[i]:
		count+=1
print (float(count)/len(y_pred))*100
