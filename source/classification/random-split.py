import sys,random

# randonly splits the input file into 2 parts, train(80%) and the test(20%)
# the test file will be used only for the final evalaution purpose. 

def write_to_file(data,label,f):

	data_file = open(f + ".csv", "w")
	data_label = open(f + "_label.csv", "w")

	for i in data:
		data_file.write(i)
	for i in label:
		data_label.write(i)

	data_file.close()
	data_label.close()


features_file = open(sys.argv[1])
label_file = open(sys.argv[2])

data_features = features_file.readlines()
data_labels = label_file.readlines()

number_of_instances = len(data_features)
length_of_test = number_of_instances / 5
length_of_train = number_of_instances - length_of_test

#print length_of_test, length_of_train, number_of_instances

store_test = random.sample(range(0,number_of_instances), length_of_test)

test = []
test_label = []

train = []
train_label = []

for i in range(0,number_of_instances):
	if i in store_test:
		test.append(data_features[i])
		test_label.append(data_labels[i])
	else:
		train.append(data_features[i])
		train_label.append(data_labels[i])
#print len(train),len(test)


write_to_file(test,test_label,"test")
write_to_file(train,train_label,"train")


features_file.close()
label_file.close()


