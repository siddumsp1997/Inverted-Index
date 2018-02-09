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



#Inverted index creation function 
def inverted_indexing():
	

	# Dictionaries declaration
	Inverted_index = {}

	name_to_id = {}
	id_to_name = {}

	i = 0


	# For calculating time for preprocessing 
	preprocessing_start_time = time.time()

	#Reading every file in alldocs folder
	for filename in os.listdir("IR_Assignment1/alldocs"):

		filepath = "IR_Assignment1/alldocs/"+str(filename)

		name_to_id[filename] = i
		id_to_name[i] = filename

		cur_file = open(filepath, "r")

		cur_file = word_by_word_processing(cur_file.read())

		cur_file = re.sub("[^a-zA-Z]+", " ", cur_file)
		tokens = nltk.tokenize.word_tokenize(cur_file)


		for token in tokens:


			if Inverted_index.__contains__(token):


				if filename not in Inverted_index[token]:

					posting_lists = Inverted_index[token]

					posting_lists[filename] = 1

					Inverted_index[token] = posting_lists

				else:

					posting_lists = Inverted_index[token]

					posting_lists[filename] += 1

					Inverted_index[token] = posting_lists

			else:

				posting_lists = {}

				posting_lists[filename] = 1

				Inverted_index[token] = posting_lists        
		
		i = i + 1            
					

	preprocessing_end_time = time.time()   

	f1 = open("part2_inverted_index_time_calc.txt",'a')

	f1.write("Time taken for preprocessing = " + str(preprocessing_end_time-preprocessing_start_time) + "secs\n")

	print("Time taken for preprocessing = " + str(preprocessing_end_time-preprocessing_start_time) + "secs\n")

	f1.close()

	with open("dictionary.p","wb") as dictionary_data1:
		pickle.dump(Inverted_index, dictionary_data1)


	# End of pre processing part


#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

	# Query processing part starts

	# f2 = open("IR_Assignment1/query.txt","r")


	# for file_query in f2:

	# 	result = [] 

	# 	print(file_query)
	# 	# Get the query ID
	# 	temp_q = file_query

	# 	x = word_tokenize(temp_q)

	# 	query_no = int(x[0])

	# 	new_text = word_by_word_processing(file_query)

	# 	query_set = new_text.split()

	# 	query_start_time = time.time()

	# 	k = 0

	# 	for query_word in query_set:
			
	# 		if k != 0:

	# 			temp_list = []

	# 			for t1 in Inverted_index[query_word].items():
	# 				temp_list.append(t1[0])

	# 			# Taking intersection of posting lists corresponding to the constituent words in the query    
	# 			result = list(set(result).intersection(set(temp_list)))


	# 		else:

	# 			for t2 in Inverted_index[query_word].items():
	# 				result.append(t2[0])   

	# 		k = k + 1 		


	# 	query_end_time = time.time()

	# 	# Calculating the time taken for this query 
	# 	query_time = query_end_time - query_start_time


	# 	f4 = open("part2_inverted_index_time_calc.txt",'a')

	# 	f4.write(str(query_no)+"  Query search time = "+str(query_time)+" secs\n")

	# 	f4.close()


	# 	f3 = open("part2_inverted_index_results.txt",'a')

	# 	for res in result:
	# 		f3.write(str(query_no) +" "+ str(res) +"\n")

	# 	f3.close() 


	# f2.close()    





#main function
if __name__ == '__main__':  
	inverted_indexing()    