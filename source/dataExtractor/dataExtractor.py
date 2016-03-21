import os
import re

fileCounter = 0

# XML file parser
def parseXMLFile(fileName):
	global fileCounter
	fileCounter += 1
	# print fileCounter, " Parsing file : ", fileName
	fr = open(fileName)
	xmlData = fr.read()
	fw = open("ExtractedBlogFiles/" + str(fileCounter) + "_blogFile" ,'w')
	xmlData = xmlData.replace('<Blog>', '').replace('</Blog>', '').replace('\n', '').replace('\r', '').replace('urlLink','')
	post_list = xmlData.split('<date>')
	blog_list = []
	for post in post_list:
		try:
			# We don't need date
			date = post.split('</date>')[0]
			# Get the blogpost
			post = post.split('<post>')[1].split('</post>')[0].strip()
			# Write to the file
			fw.write(post + '\n')			
		except:
			pass

	# Close all file handles
	fr.close();
	fw.close();
	

# Create a file for label
labelFile = open('label', 'w')

# Base directory
baseDir = "Data Sets/blogs/"

# Loop through the blog file
for file in os.listdir(baseDir):
	# check if the file ends with the xml extension
	if file.endswith(".xml"):
		# If make make an entry in the classes variable
		if re.search('\.male', file):
			labelFile.write('M\n')		
		else:
			labelFile.write('F\n')
	# parse the document
	parseXMLFile(baseDir+file)

#close label file handle
labelFile.close()

