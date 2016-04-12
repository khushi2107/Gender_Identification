'''f = open("features1.txt")
g = open("features_temp1.txt","w")
for line in f:
	data = line.split(",")
	#print len(data)
	data = [int(i) for i in data]
	req_sum = sum(data)
	if req_sum != 0:
		data = [float(i)/float(req_sum) for i in data]
	for i in range(0,len(data)-1):
		g.write(str(data[i])+",")
	g.write(str(data[-1])+"\n")'''

'''f = open("features.txt")
g= open("features_temp2.txt","w")
for line in f:
	data = line.split(",")
	data = [data[i] for i in range(0,len(data)-36)]
	for i in range(0,len(data)-1):
		g.write(data[i] + ",")
	g.write(data[-1]+"\n")'''

'''f = open("features_temp2.txt")
g = open("features_temp3.txt","w")
for line in f:
	data = line.split(",")
	data = [float(i) for i in data]
	req_sum = sum(data[-28:-8])
	#print len(range(37,57))
	for i in range(37,57):
		data[i] = float(data[i])/float(req_sum)
	del data[37]
	for i in range(0,len(data)-1):
		g.write(str(data[i]) + ",")
	g.write(str(data[-1])+"\n")'''


'''data1 = [line.strip() for line in open("features_temp3.txt", 'r')]
data2 = [line.strip() for line in open("features_temp1.txt", 'r')]
g = open("features_temp4.txt","w")
for i in range(0,len(data1)):
	temp = data1[i] + "," + data2[i]
	g.write(temp)'''

'''f = open("features_temp4.txt")
data_list = []
for i in range(0,100):
	data_list.append([])
print len(data_list)
for line in f:
	line = line.strip()
	data = line.split(",")
	for i in range(0,100):
		data_list[i].append(float(data[i]))

data_max = [max(i) for i in data_list]
data_min = [min(i) for i in data_list]
f = open("features_temp4.txt")
g = open("features_temp5.txt","w")
for line in f:
	line = line.strip()
	data = line.split(",")
	for i in range(0,len(data)-1):
		temp = (float(data[i]) - data_min[i])/(data_max[i]-data_min[i])
		g.write(str(temp) + ",")
	temp = (float(data[-1]) - data_min[-1])/(data_max[-1]-data_min[-1])
	g.write(str(temp) + "\n")'''

f = open("features_temp5.txt")
for line in f:
	line = line.strip()
	data = line.split(",")
	print len(data)