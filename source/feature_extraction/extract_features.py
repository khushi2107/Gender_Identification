import re
import os
import nltk
from collections import Counter
import numpy as np
import operator
import pickle
import sys
import math
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
POS_dic = {"CC":1, "CD":2, "DT":3, "EX":4, "FW":5, "IN":6, "JJ":7, "JJR":8, "JJS":9, "LS":10, "MD":11, "NN":12, "NNS":13, "NNP":14, "NNPS":15, "PDT":16, "POS":17,\
"PRP":18, "PRP$":19, "RB":20, "RBR":21, "RBS":22, "RP":23, "SYM":24, "TO":25, "UH":26, "VB":27, "VBD":28, "VBG":29, "VBN":30, "VBP":31, "VBZ":32, "WDT":33, "WP":34, "WP$":35, "WRB":36}

gender_set = ("actor","actress","administrator","administratrix","author","authoress","bachelor",\
			"spinster","boy","girl","BoyScout","GirlGuide","brave","squaw","bridegroom","bride","brother",\
			"sister","conuctor","conductress","count","countess","czar","czarina","dad","mum","daddy",\
			"mummy","duke","duchess","emperor","empress","father","mother","father-in-aw","mother-in-law",\
			"fiance","fiancee","gentleman","lady","giant","giantess","god","goddess","governor","matron",\
			"grandfather","grandmother","grandson","granddaughter","headmaster","headmistess","heir",\
			"heiress","hero","heroine","host","hostess","hunter","huntress","husband","wife","king",\
			"queen","lad","lass","landlord","landlady","lord","lady","male","female","man","woman",\
			"maager","manageress","manservant","maidservant","masseur","masseuse","master","mistress",\
			"mayor","mayoress","milkman","milkmaid","millionaire","millionairess","monitor","monitress",\
			"monk","nun""Mr.","Mrs.","murderer","murderess","Negro","Negress","nephew","niece","papa",\
			"mama","poet","potess","policeman","policewoman","postman","postwoman","postmaster",\
			"postmistress","priest","prietess","prince","princess","prophet","prophetess","proprietor",\
			"proprietress","prosecutor","proecutrix","protector","protectress","shepherd","shepherdess",\
			"sir","madam","son","daughter","sonin-law","daughter-in-law","step-father","step-mother",\
			"step-son","step-daughter","steward","stewardess","sultan","sultana","tailor","tailoress",\
			"testator","testatrix","uncle","aunt","usher","usherette","waiter","waitress","washerman",\
			"washerwoman","widower","widow","wizard","witch")

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
	data_string = re.sub("!{2,}","!",data_string)
	data_string = re.sub("\.{2,}",".",data_string)
	data_string = re.sub("\?{2,}","?",data_string)
	data1_tokens = nltk.word_tokenize(data_string) #tokenise the string
	to_return = []
	split=['.','?', '!']
	lower_count = 0
	upper_count = 0
	current_sentence_count = 0 
	sentence_count = 0
	word_count = 0
	punc =['.',',','?','!',';',':']
	for token in data1_tokens:
		if token in split:
			if current_sentence_count > 0:
				sentence_count+=1
			current_sentence_count = 0
		elif token not in punc:
			current_sentence_count+=1
			if current_sentence_count == 1:
				if token[0].isupper():
					upper_count+=1
				else:
					lower_count+=1
			word_count+=1
	if sentence_count == 0:
		sentence_count = 1
	to_return.append(sentence_count) #total no of sentences
	to_return.append(float(word_count)/sentence_count) #average word count of sentences
	to_return.append(float(upper_count)/sentence_count) # % of sentences with upper case starting
	to_return.append(float(lower_count)/sentence_count) # % of sentences with lower case starting
	return to_return


def get_lines_information(data_string):
	#the list of features to be returned
	#4 features
	to_return = []
	to_return.append(data_string.count("\n")) #count the number of line
	line_data = data_string.split("\n")
	punc =['.',',','?','!',';',':']
	char_count = 0
	word_count = 0
	empty_count = 0
	for i in xrange(len(line_data)):
		if line_data[i] == "":
			empty_count+=1
		else:
			char_count+=len(line_data[i])
			tokensi = nltk.word_tokenize(line_data[i])
			for j in tokensi:
				if j not in punc:
					word_count+=1
	to_return.append(float(empty_count)/to_return[0]) #count the % of empty lines
	to_return.append(float(char_count)/to_return[0]) #count the average no of characters in a line
	to_return.append(float(word_count)/to_return[0]) #count the average no fo words in a line
	return to_return

def calculate_yule_k(data_word_count,no_of_words):
	to_return = 0
	to_return = to_return + 10000.0/float(no_of_words)
	for word_count in data_word_count.keys():
		to_return = to_return + float(10000.0*(float(len(data_word_count[word_count]))*(float(word_count/no_of_words))**2))
	return to_return

def calculate_simpson_d_measure(data_word_count, no_of_words):
	to_return = 0
	for word_count in data_word_count.keys():
		to_return = to_return + float(len(data_word_count[word_count])*float(word_count)*float(word_count-1)/float(no_of_words*(no_of_words-1)))
	return to_return

def calculate_sichel_s_measure(di_hapaxs,word_set_len):
	to_return = 0
	to_return = to_return + float(float(len(di_hapaxs))/word_set_len)
	return to_return

def calculate_honore_r_measure(hapaxs,word_set_len,no_of_words):
	to_return = 0
	to_return = to_return + float(100*math.log10(no_of_words))
	to_return = to_return/float(1-float(len(hapaxs))/word_set_len)
	return to_return

def calculate_entropy_measure(data_word_count,no_of_words):
	to_return = 0
	for word_count in data_word_count.keys():
		to_return = to_return + float(len(data_word_count[word_count])*math.log10(float(no_of_words)/word_count)*float(word_count)/no_of_words)
	return to_return

def character_features(data_string):
	#the list to be returned
	#7 features
	to_return = []
	to_return.append(len(data_string)) #total no of characters
	to_return.append(float(sum(c.isalpha() and c.islower() for c in data_string))/to_return[0]) # total no of letters
	to_return.append(float(sum(c.isdigit() for c in data_string))/to_return[0]) # total no of digital characters
	to_return.append(float(sum(c.isupper() for c in data_string))/to_return[0]) #total no of upper case characters
	to_return.append(float(sum(c.isspace() for c in data_string))/to_return[0]) #total no of whitespace characters
	to_return.append(float(data_string.count('\t'))/to_return[0]) # total no of tab space characters
	to_return.append(float(1-to_return[1]-to_return[2]-to_return[3]-to_return[4]-to_return[5])) # total no of special characters
	return to_return

def syntactic_features(data_string,no_of_characters):
	#the list of features to be returned
	#10 features
	to_return = []
	to_return.append(float(data_string.count("'"))/no_of_characters) #count of ' char
	to_return.append(float(data_string.count(","))/no_of_characters) #count of , char
	to_return.append(float(len(re.findall("\.{2,}",data_string)))/no_of_characters) #counts of multiple times occuring . char
	data_string = re.sub("\.{2,}"," ",data_string) #remove the multiple times occuring . char
	to_return.append(float(data_string.count('.'))/no_of_characters) #count of . char
	to_return.append(float(data_string.count(';'))/no_of_characters) #count of ; char
	to_return.append(float(data_string.count(':'))/no_of_characters) #count of : char
	to_return.append(float(len(re.findall("\?{2,}",data_string)))/no_of_characters) #counts of multiple times occuring ? char
	data_string = re.sub("\?{2,}"," ",data_string) #remove the multiple times occuring ? char
	to_return.append(float(data_string.count('?'))/no_of_characters) #count of ? char
	to_return.append(float(len(re.findall("!{2,}",data_string)))/no_of_characters) #counts of multiple times occuring ! char
	data_string = re.sub("!{2,}"," ",data_string) #remove the multiple times occuring ! char
	to_return.append(float(data_string.count('!'))/no_of_characters) #count of ! char
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

def word_based_features(data_string):
	#the list of features to be returned
	#currently features
	#TODO not complete yet..
	punctuations = ['.',',','?','!',';',':']
	to_return = []
	data_tokens = nltk.word_tokenize(data_string.lower()) #tokenise the string
	data_tokens = [i for i in data_tokens if i not in punctuations and i != '']
	data_tokens_set = set(data_tokens)
	data_tokens_len = [float(len(i)) for i in data_tokens] #get tokens length
	data_tokens_larger_6 = [i for i in data_tokens if len(i)>6] #get tokens of length > 6
	data_tokens_small = [i for i in data_tokens if len(i) < 4] #get tokens of length < 4
	data_count = Counter(data_tokens)
	data_count_dict = dict(data_count) #get count of each token
	data_word_count = {}
	for i in data_count_dict.keys():
		try:
			data_word_count[data_count_dict[i]].append(i)
		except KeyError:
			data_word_count[data_count_dict[i]] = []
			data_word_count[data_count_dict[i]].append(i)
	hapaxs = [i for i in data_count_dict.keys() if data_count_dict[i] == 1] #get the hapax words... for info see https://en.wikipedia.org/wiki/Hapax_legomenon
	di_hapaxs = [i for i in data_count_dict.keys() if data_count_dict[i] == 2]
	to_return.append(len(data_tokens)) #no of words
	to_return.append(sum(data_tokens_len)/float(len(data_tokens_len))) #average length of words
	to_return.append(float(len(set(data_tokens)))/float(len(data_tokens))) #no of distinct words, vocabulary strength
	to_return.append(float(len(data_tokens_larger_6))/float(len(data_tokens))) #no of words with length > 6
	to_return.append(float(len(data_tokens_small))/float(len(data_tokens))) #no of words with length < 4
	to_return.append(float(len(hapaxs))/float(len(data_tokens))) #hapax legomena
	to_return.append(float(len(di_hapaxs))/float(len(data_tokens))) #hapax dislegomena
	to_return.append(calculate_yule_k(data_word_count,len(data_tokens))) #yule's k measure
	to_return.append(calculate_simpson_d_measure(data_word_count,len(data_tokens))) #simpsons d measure
	to_return.append(calculate_sichel_s_measure(di_hapaxs,len(data_tokens_set))) #sichels s measure
	to_return.append(calculate_honore_r_measure(hapaxs,len(data_tokens_set),len(data_tokens))) #honores r measure
	to_return.append(calculate_entropy_measure(data_word_count,len(data_tokens))) #calculate the entropy measure
	return to_return	

''' Fucntion words extraction '''
def function_words_features(data_string):
	# Tokenize the blog
	tokened_data_string = nltk.word_tokenize(data_string)
	# Get the count of words
	total_words = len(tokened_data_string)
	to_return = []
	# Tag the text
	postagtext = nltk.pos_tag(tokened_data_string)
	# Article words
	to_return.append(float(str(postagtext).count('DT'))/float(total_words))
	# Prosentense words
	to_return.append(float((data_string.lower().count('yes') + data_string.lower().count('no') + data_string.lower().count('okay') + data_string.lower().count('ok')))/float(total_words))
	# Pronoun words
	total_pronouns = str(postagtext).count('PP') + str(postagtext).count('PP$') + str(postagtext).count('WP') + str(postagtext).count('WP$')
	to_return.append(float(total_pronouns)/float((total_words)))
	# Auxilary Verbs
	to_return.append(float((str(postagtext).count('VB') + str(postagtext).count('VBD') + str(postagtext).count('VBG') + str(postagtext).count('VBN') + str(postagtext).count('VBP') + str(postagtext).count('VBZ'))) / float(total_words))
	# Conjunction words
	to_return.append(float(str(postagtext).count('CC'))/float(total_words))
	# interjection words
	to_return.append(float(str(postagtext).count('UH'))/float(total_words))
	# adposition words
	to_return.append(float(str(postagtext).count('IN'))/float(total_words))
	# gender-specific words
	count=0
	for word in tokened_data_string:
		if word in gender_set:
			count+=1;
	to_return.append(float(count)/float(total_words))
	return to_return

def extract_features(filename):
	#rading data from the file
	with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as fdata:
		data1 = fdata.read()
	#data1 = data1.decode('cp1250')
	data1 = data1.encode('utf-8',errors='ignore') 
	data1 = re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, data1) #remove the buggy encodings.. see the big list :P
	data1 = data1.replace("\0x93",'"')
	data1 = data1.replace("\0x94",'"')
	data1 = data1.decode('utf-8')
	#the feature vector
	feature = []
	feature.extend(character_features(data1)) #extend the feature vector with character features
	feature.extend(syntactic_features(data1,feature[0])) #extend the feature vector with syntactic features
	feature.extend(structural_features(data1)) #extend the feature vector with structural features
	feature.extend(word_based_features(data1)) #extend the feature vector with word based features
	return feature

if __name__=="__main__":
	feature_file = open("features.txt", "wb")
	for i in range(1,19321):
		features = extract_features("../../../IRE/ExtractedBlogFiles/" + str(i) + "_blogFile")
		for j in range(0,len(features)-1):
			feature_file.write(str(features[j])+",")
		feature_file.write(str(features[-1]) + "\n")
	feature_file.close()
