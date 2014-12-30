import json
import shelve
from evaluate_comment import *
import nltk
import sys
import gensim
from gensim.models import Word2Vec
from sklearn import svm
from sklearn.cluster import *
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
from nltk import *
# Input file with text for the business, trained word2vec model address, trained svm address
# Returns a list of lists with each item denoting a sentence
# The inner list for each sentence contains:
# 1. Ambience P/A 2. Ambience Probability 3. Food P/A 4. Food Probability  Simialrly for Serice and VFM at 5,6,7,8
# 9. Polarity
def return_similaritymat(address,word2vec,svm_model):
	file=(address)
	matrix=[]
	count=0
	for line in file:
		count=count+1
		print(count)
		if(len(line)>0):
			ret=eval_comment(line,word2vec,svm_model)
			for l in ret:
				out=[]
				out.append(l['Ambience'][0])
				out.append(l['Ambience'][1])
				out.append(l['Food'][0])
				out.append(l['Food'][1])
				out.append(l['Service'][0])
				out.append(l['Service'][1])
				out.append(l['VFM'][0])
				out.append(l['VFM'][0])
				out.append(l['Polarity'])
				matrix.append(out)
	return matrix
print(return_similaritymat('business_reviews.json','model.txt','svm.pkl'))

# Function to train classifiers for existance or non-existance of class in the sentence
# The inputs to the vector are 1: Path to labelled data file 
#2: Path to word2vec file
#3: Output shelve file for storing the trained objects

def training(labelled_data,vec_model,output_file):
    topics=["Ambience","Food","Service","VFM"]
    tps=[["ambinece","experience","atmosphere"],["food","cook","flavour"],["service","staff","time"],["price","worth","free","deal","satisfaction"]]
    file=open(labelled_data) 
    model=Word2Vec.load(vec_model)
    obj=json.loads(file.read())
    # Kmeans clustering
    cluster=[[],[],[],[]]
    for review in obj:
        # Review model
        sentence=sent_tokenize(review[2])
        for sent in sentence:
            words=nltk.word_tokenize(sent)
            phrase=review[4]
            for word in words:
                high=[]
                high_topic=[]
                tp=-1
                for topic in topics:
                    tp=tp+1
                    for tapic in tps[tp]:
                        try:
                            high.append(model.similarity(tapic,word))
                        except:
                            high.append(0)
                        high_topic.append(tp)
                maxi=max(high)
                maxi_index=high.index(maxi)
                maxi_topic=high_topic[maxi_index]
                # Assiging the cluster weights for every word
                for tp in range(0,4):
                    if(tp==maxi_topic): 
                        cluster[tp].append([maxi])
                    else:
                        cluster[tp].append([0])
    # K-Means clustering Implementation 
    clus=[[],[],[],[]]
    tp=-1
    for topic in topics:
        tp=tp+1
        clus[tp]=KMeans()
        clus[tp].fit(cluster[tp])
# Review iterator
    train=[[],[],[],[]]
    output=[[],[],[],[]]
    for review in obj:
    # Review model
    # Tagging for presence of category in sentece
        sentence=sent_tokenize(review[2])
        for sent in sentence:
            tp=-1
            words=nltk.word_tokenize(sent.lower())
            phrase=review[4]
            for topic in topics:
                tp=tp+1
                if(type(phrase['phrase'][topic])== tuple or type(phrase['phrase'][topic])== list):
                    phr=-1
                    found=0
                    for ph in phrase['phrase'][topic]:
                        phr=phr+1
                        if(ph in sent):
                            found=1
                    if(found==1):       
                        output[tp].append(1)
                    else:
                        output[tp].append(0)
                else:
                    if(phrase['phrase'][topic] in sent):
                        output[tp].append(1)
                    else:
                        output[tp].append(0)
            sent_index=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
            # Finding frequency distribution for each sentence
            for word in words:
                high=[]
                high_topic=[]
                tp=-1
                for topic in topics:
                    tp=tp+1
                    for tapic in tps[tp]:
                        try:
                            high.append(model.similarity(tapic,word))
                        except:
                            high.append(0)
                        high_topic.append(tp)
                maxi=max(high)
                maxi_index=high.index(maxi)
                maxi_topic=high_topic[maxi_index]
                for tp in range(0,4):
                    if(tp==maxi_topic): 
                        ind=clus[tp].predict([maxi])
                    else:
                        ind=clus[tp].predict([0])
                    sent_index[tp][ind]=sent_index[tp][ind]+1
            # Adding the frequency vectors      
            for tp in range(0,4):
                train[tp].append(sent_index[tp])
    print(len(train[1]))
    print(len(output[1]))
    # List for svm objects          
    cls=[[],[],[],[]]
    tp=-1
    for topic in topics:
        tp=tp+1
        cls[tp]=svm.SVC(probability=True)
        cls[tp].fit(train[tp],output[tp])
    svms=shelve.open(output_file)
    svms['svm']=cls
    svms['km']=clus
    svms.close()
#Method to evaluate a single comment
# input 
#text,vec_model,output_file: review, Word2vec model address,trained svm 
def eval_comment(text,vec_model,output_file):
	topics=["Ambience","Food","Service","VFM"]
	tps=[["ambinece","experience","atmosphere"],["food","cook","flavour"],["service","staff","time"],["price","worth","free","deal","satisfaction"]]
	#Open trained svm objects
	mat=shelve.open(output_file)
	cls=mat['svm']
	clus=mat['km']
	model=Word2Vec.load(vec_model)
	comment=[]
	blob=TextBlob(text)
	for sentence in blob.sentences:
		sent={}
		sent_index=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
		words=sentence.lower()
		words=words.words
		# Finding the best simialriry of each word
		for word in words:
			high=[]
			high_topic=[]
			tp=-1
			for topic in topics:
				tp=tp+1
				for tapic in tps[tp]:
					try:
						high.append(model.similarity(tapic,word))
					except:
						high.append(0)
					high_topic.append(tp)
			maxi=max(high)
			maxi_index=high.index(maxi)
			maxi_topic=high_topic[maxi_index]
			# Finding frequency distribution of similarity index in sentence
			for tp in range(0,4):
				if(tp==maxi_topic):	
					ind=clus[tp].predict([maxi])
				else:
					ind=clus[tp].predict([0])
				sent_index[tp][ind]=sent_index[tp][ind]+1
		# Adding the svm classification results
		for tp in range(0,4):
			out=cls[tp].predict(sent_index[tp])
			out_pro=cls[tp].predict_proba(sent_index[tp])	
			sent[topics[tp]]=[out,out_pro[0][out]]
		# Adding sentence polarity results using TextBlob
		if(sentence.sentiment.polarity>0):
			sent['Polarity']=1
		else:
			sent['Polarity']=-1
		comment.append(sent)
	return(comment)

