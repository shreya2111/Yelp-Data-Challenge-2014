# Read every comment from the corpus 
import gensim
import json
from nltk.tokenize import sent_tokenize
import nltk
# File for creating word2vec model from the text 
#Inputs
# input_text,outputadd: Address to text corpus to train on, Output model file
def word2vec_train(input_text,outputadd):
    class MySentences(object):
        def __init__(self, dirname):         
            self.dirname = dirname
        def __iter__(self):
            file=open(self.dirname)
            obj=json.loads(file.read())
            count=0
            for review in obj:
                count=count+1
                text=review['text']
                sentences=sent_tokenize(text.lower())   
                for line in sentences:
                    yield line.split()
    sentences = MySentences(input_text) # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences)
    model.save(outputadd)