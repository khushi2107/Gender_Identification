from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
import numpy as np
from sklearn import decomposition
from collections import Counter
import pickle


def classify_input(data):
	data = np.array(data)
	data = [data, data]
	data = np.array(data)
	outs = []

	#Randm Forest Classifier
	rfc = pickle.load( open( "random_forest.p", "rb" ) )
	outs.append(rfc.predict(data)[0])

	#Neural Network Classifier
	nnc = pickle.load( open( "neural_network.p", "rb" ) )
	outs.append(nnc.predict(data)[0])

	##Adaboost Tree Classifier
	atc = pickle.load( open( "adaboost_tree.p", "rb" ) )
	outs.append(atc.predict(data)[0])

	#Gradient Boosting Classifier
	gbc = pickle.load( open( "gradient_boost.p", "rb" ) )
	outs.append(gbc.predict(data)[0])

	#Bagging Classifier
	bac = pickle.load( open( "bagging.p", "rb" ) )
	outs.append(bac.predict(data)[0])

	count = Counter(outs)
	return count.most_common()[0][0]