f = open("features_temp4.txt")
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
	g.write(str(temp) + "\n")
