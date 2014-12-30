The topic identification matrix generation has the following files for the following components
1. word2vec.py: This file contains functions for training of word2vec model from Yelp reviews
2. matrix_generation.py: This file containes all the functions for matrix_geneartion
	1. return_similaritymat : Returns calls other functions to return the similarity matrix
		# Returns a list of lists with each item denoting a sentence
		# The inner list for each sentence contains:	
		# 1. Ambience P/A 2. Ambience Probability 3. Food P/A 4. Food Probability  Simialrly for Serice and VFM at 5,6,7,8
		# 9. Polarity
	2. training: Trains the svm on the given labelled comments and create a shelve file with trained object
3. model.txt: Trained word2vec model
4. svm.pkl: trained svm objects file
5. Labelled_Data: Labelled reviews to train the svm
6. business_reviews: All the text reviews for a particualr restaurant business
