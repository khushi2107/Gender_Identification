import re
import os
import nltk
from collections import Counter
import numpy as np
import operator
import pickle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
POS_dic = {"CC":1, "CD":2, "DT":3, "EX":4, "FW":5, "IN":, "JJ":7, "JJR":8, "JJS":9, "LS":10, "MD":11, "NN":12, "NNS":13, "NNP":14, "NNPS":15, "PDT":16, "POS":17,/
 "PRP":18, "PRP$":19, "RB":20, "RBR":21, "RBS":22, "RP":23, "SYM":24, "TO":25, "UH":26, "VB":27, "VBD":28, "VBG":29, "VBN":30, "VBP":31, "VBZ":32, "WDT":33, "WP":34, "WP$":35, "WRB":36}

#handling of the unwanted unicodes
chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : '',          # modifier - under line
    '\xc3\x80' : 'A',
    '\xc3\x81' : 'A',
    '\xc3\x82' : 'A',
    '\xc3\x83' : 'A',
    '\xc3\x84' : 'A',
    '\xc3\x85' : 'A',
    '\xc3\x86' : 'AE',
    '\xc3\x87' : 'C',
    '\xc3\x88' : 'E',
    '\xc3\x89' : 'E',
    '\xc3\x8a' : 'E',
    '\xc3\x8b' : 'E',
    '\xc3\x8c' : 'I',
    '\xc3\x8d' : 'I',
    '\xc3\x8e' : 'I',
    '\xc3\x8f' : 'I',
    '\xc3\x90' : 'D',
    '\xc3\x91' : 'N',
    '\xc3\x92' : 'O',
    '\xc3\x93' : 'O',
    '\xc3\x94' : 'O',
    '\xc3\x95' : 'O',
    '\xc3\x96' : 'O',
    '\xc3\x97' : 'x',
    '\xc3\x99' : 'U',
    '\xc3\x9a' : 'U',
    '\xc3\x9b' : 'U',
    '\xc3\x9c' : 'U',
    '\xc3\x9d' : 'Y',
    '\xc3\xa0' : 'a',
    '\xc3\xa1' : 'a',
    '\xc3\xa2' : 'a',
    '\xc3\xa3' : 'a',
    '\xc3\xa4' : 'a',
    '\xc3\xa5' : 'a',
    '\xc3\xa6' : 'ae',
    '\xc3\xa7' : 'c',
    '\xc3\xa8' : 'e',
    '\xc3\xa9' : 'e',
    '\xc3\xaa' : 'e',
    '\xc3\xab' : 'e',
    '\xc3\xac' : 'i',
    '\xc3\xad' : 'i',
    '\xc3\xae' : 'i',
    '\xc3\xaf' : 'i',
    '\xc3\xb1' : 'n',
    '\xc3\xb2' : 'o',
    '\xc3\xb3' : 'o',
    '\xc3\xb4' : 'o',
    '\xc3\xb5' : 'o',
    '\xc3\xb6' : 'o',
    '\xc3\xb9' : 'u',
    '\xc3\xba' : 'u',
    '\xc3\xbb' : 'u',
    '\xc3\xbc' : 'u',
    '\xe2\x80\x9c' : '"',
    '\xe2\x80\x9d' : '"',
    '\xe2\x80\x99' : "'",
    '\xe2\x80\x94' : "-",
    '\xe2\x80\x98' : "'"
}

#function for handling the unicodes
def replace_chars(match):
    char = match.group(0)
    return chars[char]

def get_sentence_information(data_string):
	#the list of feature to be returned
	#4 features
    data1_tokens = nltk.word_tokenize(data_string) #tokenise the string
	split=['.','?']
	lower_count = 0
	upper_count = 0
	current_sentence_count = 0
	sentence_count = 0
	punc =['.',',','?','!',';',':']
	for token in data_tokens:
		if token in split:
			if current_sentence_count > 0:
				sentence_count+=1
			current_sentence_count = 0
		elif token not in punc:
			current_sentence_count+=1
			if current_sentence_count == 1:
				if token[0].isupper():
					upper_count+=1
				else
					lower_count+=1
			word_count+=1
	to_return.append(sentence_count) #total no of sentences
	to_return.append(float(word_count)/sentence_count) #average word count of sentences
	to_return.append(float(upper_count)/sentence_count) # % of sentences with upper case starting
	to_return.append(float(lower_count)/sentence_count) # % of sentences with lower case starting


def get_lines_information(data_string):
	#the list of features to be returned
	#4 features
	to_return = []
	to_return.append(data_string.count("\n")) #count the number of line
	line_data = data_string.split("\n")
	punc =['.',',','?','!',';',':']
	char_count = 0
	word_count = 0
	for i in xrange(len(line_data)):
		if line_data[i] == "":
			empty_count+=1
		else:
			char_count+=len(i)
			tokensi = nltk.word_tokenize(i)
			for j in tokensi:
				if j not in punc:
					word_count+=1
	to_return.append(float(empty_count)/to_return[0]) #count the % of empty lines
	to_return.append(float(char_count)/to_return[0]) #count the average no of characters in a line
	to_return.append(float(word_count)/to_return[0]) #count the average no fo words in a line
	return to_return


def syntactic_features(data_string,no_of_characters):
	#the list of features to be returned
	#10 features
	to_return = []
	to_return.append(float(data_string.count("'"))/no_of_characters) #count of ' char
	to_return.append(float(data_string.count(","))/no_of_characters) #count of , char
	to_return.append(float(len(re.findall("\.{2,}",data_string)))/no_of_characters) #counts of multiple times occuring . char
	data_string = re.sub("\.{2,}"," ",data_string) #remove the multiple times occuring . char
	to_return.append(float(len(data_string.count('.')))/no_of_characters) #count of . char
	to_return.append(float(len(data_string.count(';')))/no_of_characters) #count of ; char
	to_return.append(float(len(data_string.count(':')))/no_of_characters) #count of : char
	to_return.append(float(len(re.findall("\?{2,}",data_string)))/no_of_characters) #counts of multiple times occuring ? char
	data_string = re.sub("\?{2,}"," ",data_string) #remove the multiple times occuring ? char
	to_return.append(float(len(data_string.count('?')))/no_of_characters) #count of ? char
	to_return.append(float(len(re.findall("!{2,}",data_string)))/no_of_characters) #counts of multiple times occuring ! char
	data_string = re.sub("!{2,}"," ",data_string) #remove the multiple times occuring ! char
	to_return.append(float(len(data_string.count('!')))/no_of_characters) #count of ! char
	return to_return

def structural_features(data_string):
	#the list of features to be returned
	#currently 8 features
	#TODO do for paragraphs....
	#TODO greeting and farewell words
	to_return = []
	to_return.extend(get_lines_information(data_string))
	to_return.extend(get_sentence_information(data_string))
	return to_return


def extract_features(filename):
	#rading data from the file
	with open (filename, "r") as myfile1:
        data1 = myfile1.read()
    data1 = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, data1) #remove the buffy encodings.. see the big list :P
    #the feature vector
    feature = []
    #extend the feature vector with syntactic features
    feature.extend(syntactic_features(data1))
    #extend the feature vector with structural features
    feature.extend(structural_features(data1_tokens))
