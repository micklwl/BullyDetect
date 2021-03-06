import time 
import pickle
import os
import logging
import datetime
import multiprocessing

import numpy as np 

from gensim.models import Word2Vec as w2v 
from sklearn.cluster import KMeans, MiniBatchKMeans

# Set seed
seed = 7
np.random.seed(seed)

def doClustering():

	os.system('cls')

	# Load Word2Vec model
	print("LOADING WORD2VEC MODEL \n\n")
	model = w2v.load_word2vec_format('W2V Models/w2v_reddit_unigram_300d.bin', binary=True)

	# Specify the number of words and clusters (250,500,1000,2000,4000)
	#WORDS = 1000000
	CLUSTERS = 500

	# Get the word vectors and the word
	print("GETTING WORD VECTORS AND WORDS \n\n")
	word_vectors = model.syn0
	words = model.index2word

	# Delete the model to clear up memory
	print("DELETING WORD2VEC MODEL AND SLEEPING \n\n")
	del model
	time.sleep(10)

	# Initialize K-Means
	k_means = KMeans( n_clusters = CLUSTERS, n_jobs= -2, precompute_distances=True)
	#k_means = MiniBatchKMeans(n_clusters = CLUSTERS)

	# Give starting time of initialization
	start = datetime.datetime.now()
	print("STARTING AT: %i/%i/%i %i:%i \n" % (start.month, start.day, start.year, start.hour, start.minute))

	# Fit the model, get the centroid number and calculate time
	print("TRAINING K-MEANS WITH %i CLUSTERS \n\n" % (CLUSTERS))
	start = time.time()
	idx = k_means.fit_predict(word_vectors)
	end_time = time.time()

	# Display ending time of fitting
	end = datetime.datetime.now()
	print("ENDING AT:  %i/%i/%i %i:%i" % (end.month, end.day, end.year, end.hour, end.minute))
	print("TIME TAKEN: ", end_time-start)

	# Create a Word / Index dictionary
	# Each vocabulary word is matched to a cluster center
	# Motivation: https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-3-more-fun-with-word-vectors
	word_centroid_map = dict(zip(words,idx))

	# Save the dictionary
	print("\n\nSAVING MODEL")
	FILE = "K-Means Models/full_" + str(CLUSTERS) + "C.pk"
	pickle.dump(word_centroid_map, open(FILE, "wb"))

if __name__ == '__main__':

	doClustering()