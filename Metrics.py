import specificity as sp
import json
import os
import numpy
import math

def metric1(matrix,L_of_constructs):
	try:
		#print "Inside metric one"
	
		length = len(matrix[0])
		num_of_constructs = len(L_of_constructs)
		constructs = []
		coverage = []
		done = 0
		inputtext_length = len(matrix)
		matrices = [[]]


		for i in range(num_of_constructs):
			if i==0:
				MATRIX = matrix[:,0:L_of_constructs[i]]
				matrices.append(MATRIX)
				done = done+L_of_constructs[i]
				diag = numpy.diagonal(MATRIX)
				## Check if this is a good construct
				if 0 in diag:
					pass
				else:
					# If yes, remember the i value of this sub matrix
					constructs.append(i)
				# In any case, calculate the coverage
				num_of_words = 0
				for k in range(len(MATRIX)):
					if 1 in MATRIX[k]:
						num_of_words = num_of_words + 1
		
				coverage.append(num_of_words)

			if i>0:
				MATRIX = matrix[:,done:done+L_of_constructs[i]]
				matrices.append(MATRIX)
				done = done+L_of_constructs[i]
				diag = numpy.diagonal(MATRIX)
				if 0 in diag:
					pass
				else:
					constructs.append(i)
				num_of_words = 0
				for k in range(len(MATRIX)):
					if 1 in MATRIX[k]:
						num_of_words = num_of_words + 1
		
				coverage.append(num_of_words)

		max_coverage = max(coverage)
		metric1 = []

		for i in range(len(coverage)):
			metric1.append(round(float(coverage[i])/float(max_coverage),2))
		#print metric1

		return metric1,coverage
	except Exception as e:
		pass 
	


#def metric2(Overall_semantic):
#	return round(m2,2)

def metric3(slots, arr):
	#if slots is like, slots=['agent','object'] or ['agent','action','complex object'], #of slots in cons=2 or 3
	#one cons=['action','object','agent'] #with all the slots	
	#print "inside metric three"

	#print s
	m3=sum(arr)/len(slots)
	return round(m3,2)

def metric4(s,slots):
	
	#Words that are in the construction,words=['eat','pray','love']
	#print "inside metric four"
	
	m4=sum(s)/len(slots)
	return round(m4,2)

def confidence(m):
	if max(m)==0:
		return 0
	else:
		return round((m[-1]-m[-2])/m[-1],2)
	

def quality(confidence,words_covered,total_words):
	Ratio=round((words_covered/total_words),6)
	q=(1-math.exp(-Ratio*12))+(Ratio*math.exp(-12))*(1-math.exp(-confidence*16))+(confidence*math.exp(-16))
	return round(q,4)

	
