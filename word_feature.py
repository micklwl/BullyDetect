import pandas as pd 
import numpy as np 
import os

from gensim.models import Word2Vec as w2v

from evaluation import evaluate

# Use each word as a feature
def makeFeatureVec(comment, model, num_features):

	# Pre-initialize an empty numpy array (for speed)
	featureVec = np.zeros((num_features,),dtype="float32")

	# Loop word-by-word, as well as index
	for i,word in enumerate(comment.split()):

		# INCOMPLETE SENTENCE DETECTED
		if i == len(featureVec):
			break

		# If word is in model, return average of the word's feature vectors
		# Else, return -1 which indicates no word found
		if word in model:
			word_feature = np.mean(model[word])
		else:
			word_feature = -1.0

		# Overwrite the sentence of the numpy array
		featureVec[i] = word_feature

	return featureVec

# One of the kaggle tests
def commentFeatureVecs(comments, model, num_features):

	# Initialize empty counter
	counter = 0

	# Preallocate a 2D numpy array for speed
	reviewFeatureVecs = np.zeros((len(comments),num_features),dtype="float32")

	for comment in comments:

		# Call function that gets the average vectors
		reviewFeatureVecs[counter] = makeFeatureVec(comment, model, num_features)

		# Increment counter
		counter += 1


	return reviewFeatureVecs


os.system('cls')

# Load Word2Vec model here
print("LOADING WORD2VEC MODEL\n\n")
FILE = "W2V Models/w2v_reddit_unigram_300d.bin"
model = w2v.load_word2vec_format(FILE, binary=True)

# Load the dataset here
df = pd.read_csv('balanced_dataset.csv')

# Separate out comments and labels
X , y = df['Comment'], df['Insult']

# Transform the data
print("TRANSFORMING DATA \n\n")
MAX_WORDS = 300
X = commentFeatureVecs(X, model, MAX_WORDS)

# Get the Python's file name. Remove the .py extension
file_name = os.path.basename(__file__)
file_name = file_name.replace(".py","")

# Evaluate models 
evaluate(X,y, file_name)