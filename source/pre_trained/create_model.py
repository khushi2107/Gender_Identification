from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
import numpy as np
from sklearn import decomposition
from collections import Counter
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

#Random Forest
rfc = RandomForestClassifier(n_estimators=300)
clf = rfc.fit(data,labels)
pickle.dump( clf, open( "random_forest.p", "wb" ) )

#Neural Networks
nnc = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(10,2), random_state=1)
clf = nnc.fit(data,labels)
pickle.dump( clf, open( "neural_network.p", "wb" ) )

#Adaboost Tree Classifier
atc = AdaBoostClassifier(n_estimators=300)
clf = atc.fit(data, labels)
pickle.dump( clf, open( "adaboost_tree.p", "wb" ) )

#Gradient Boosting Classifier
gbc = GradientBoostingClassifier(n_estimators=300)
clf = gbc.fit(data,labels)
pickle.dump( clf, open( "gradient_boost.p", "wb" ) )

#Bagging Classifier
bac = BaggingClassifier(n_estimators=300)
clf = bac.fit(data,labels)
pickle.dump( clf, open( "bagging.p", "wb" ) )