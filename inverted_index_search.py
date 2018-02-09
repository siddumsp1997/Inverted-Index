#import the necessary packages
import sys  
import os
import time
import nltk
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer, WordNetLemmatizer


# Processing line and converting it to tokens
def word_by_word_processing(line):
	
	
	line = re.sub("[^a-zA-Z]+", " ", line)

	set_of_stop_words = nltk.corpus.stopwords.words('english')

	stem_ob = nltk.stem.porter.PorterStemmer()

	tokenset = nltk.tokenize.word_tokenize(line)

	#final_set_of_tokens = []

	final_line = ""

	for token in tokenset:

		token = token.lower()

		if token not in set_of_stop_words:

			final_line += stem_ob.stem(token)
			final_line += " "       
		
	return final_line



#Inverted index search function 
def inverted_index_search():
	
	#Loading the dictionary from the pickle file
	with open("dictionary.p","r") as dictionary_data:
		Inverted_index = pickle.load(dictionary_data)
	

	f2 = open("IR_Assignment1/query.txt","r")


	for file_query in f2:

		result = [] 

		# Get the query no
		temp_q = file_query

		#print(query)
		x = word_tokenize(temp_q)

		query_no = int(x[0])

		new_text = word_by_word_processing(file_query)

		query_set = new_text.split()

		#print(query_set)

		query_start_time = time.time()

		k = 0

		for query_word in query_set:
			
			if k != 0:

				temp_list = []

				for t1 in Inverted_index[query_word].items():
					temp_list.append(t1[0])

				# Taking intersection of posting lists corresponding to the constituent words in the query    
				result = list(set(result).intersection(set(temp_list)))


			else:

				for t2 in Inverted_index[query_word].items():
					result.append(t2[0])   

			k = k + 1 		


		query_end_time = time.time()

		# Calculating the time taken for this query 
		query_time = query_end_time - query_start_time


		f4 = open("inverted_index_time_calc.txt","a")

		f4.write(str(query_no)+"  Query search time = "+str(query_time)+" secs\n")

		f4.close()


		f3 = open("inverted_index_output.txt","a")

		for res in result:
			f3.write(str(query_no) +" "+ str(res) +"\n")

		f3.close() 


	f2.close()    





#main function
if __name__ == '__main__':  
	inverted_index_search()    
