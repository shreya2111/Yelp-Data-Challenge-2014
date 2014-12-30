from __future__ import division
import os
import json
import numpy
from senticnet.senticnet import Senticnet
import gensim

def S(words):
	sn = Senticnet()
	os.chdir('dataset/')
	model = gensim.models.Word2Vec.load('mymodel')
	os.chdir('../')

	#words = ["eat", "pray", "love"]
	counter = [0 for x in words]
	children = [[] for i in range(len(words))]
	total_words=[[] for i in range(len(words))]
	for i in range(len(children)):
		children[i].append(words[i])
		total_words[i].append(words[i])


	for i in range(len(words)):
		#print "WORD: ", words[i]
		# print "Specificity of ", words[i]
		semantics1 = []
		try:
			semantics1 = sn.semantics(words[i])
			for t in semantics1:
				total_words[i].append(t)

		except:
			pass
		for k in range(len(semantics1)):
			sim = 0
			try:
				sim = model.similarity(words[i], semantics1[k])
			except KeyError as e:
				pass
			if (sim >= 0.1) and (semantics1[k] not in children[i]):
				counter[i] = counter[i] + 1
				#print semantics1[k]
				children[i].append(semantics1[k])
				semantics2 = []
				try:
					semantics2 = sn.semantics(semantics1[k])
					#print semantics2,"total words are: ",total_words[i]
					#tmp=getMatch(semantics2,total_words[i])
					#print "tmp: ",tmp
					for t in semantics2:
						if t not in total_words[i]:
							total_words[i].append(t)
					#print "total words: ",total_words[i]
				except:
					pass
				for j in range(len(semantics2)):
					sim = 0
					try:
						sim = model.similarity(words[i], semantics2[j])
					except KeyError as e:
						pass
					if sim >= 0.1 and (semantics2[j] not in children[i]):
						counter[i] = counter[i] + 1
						#print semantics2[j]
						children[i].append(semantics2[j])
						semantics3 = []
						try:
							semantics3 = sn.semantics(semantics2[j])

							#tmp=getMatch(semantics3,total_words[i])
							for t in semantics3:
								if t not in total_words[i]:
									total_words[i].append(t)
							#print semantics3,"total words are: ",total_words[i]
						except:
							pass
						for l in range(len(semantics3)):
							sim = 0
							try:
								sim = model.similarity(words[i], semantics3[l])
							except KeyError as e:
								pass
							if sim >= 0.1 and (semantics3[l] not in children[i]):
								counter[i] = counter[i] + 1
								#print semantics3[l]
								children[i].append(semantics3[l])

	s=[0 for x in words]

	for i in range(len(children)):
		if len(children[i])<1 and len(total_words[i])>=1:
			#print "Child"
			s[i]=1 #child node
		elif len(children[i])>=1 and len(total_words[i])>1:
			#print "element is not a child node"
			s[i]=1-round((len(children[i])/len(total_words[i])),2) #element is not a child node
		elif len(children[i])<1 and len(total_words[i])<1:
			#print "element is not found"
			s[i]=0 #element not found
		else:
			#print "in else"
			s[i]=0	
	
	return s		
		
