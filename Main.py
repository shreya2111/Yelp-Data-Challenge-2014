import nltk
import json
import os
import Metrics as Mt
import numpy
import time
import specificity as sp
import conceptnet_req as cnet

os.chdir('dataset/')
f=open('const_sentences.json','r')
data=json.load(f)  #Reviews for a business broken into short sentences
f.close()
os.chdir('../')
output=[]
F = []

try:
	type_cons = ['action', 'agent', 'loc', 'location', 'description', 'object']
	specificities_of_cons = zip(type_cons, sp.S(type_cons))

	constructions=[['action','object'],['action','loc','location'],['agent','action','loc','location'],['agent','action','object'],['agent','action','description'],['agent','action','loc','object'],['action','agent'],['action','object','description'],['agent','action','description'],['agent','loc','location','description'],['agent','loc','location','action','description']]


	
	for a in data:

		#Each review is a set of review id, rating, review text
		input_sentence=[]
		# Retrieving labelled data
		words=a[1].split()
		print "Words: ",words
		specificities = sp.S(words)
		specificities_of_words = zip(words, specificities)
		for i in range(len(a[0])):

			tag=a[0][i][0]

			if len(a[0][i])>1:
				for word in words:

					if word in a[0][i]:
						input_sentence.append(tag)			
			else:	
		
				pass
		
		tagged_words = zip(words, input_sentence)


		if words!=[] and len(words)<=10 and tagged_words!=[]:
			start_time = time.time()
			
			rows=len(words) # words in rows 

			#Define constructions and overall prototypes	
		
			sum_x=0	
			columnnames = []
			for x in constructions:
				sum_x+=len(x)
				for slotname in x:
					columnnames.append(slotname)
			#print rows,sum_x


			#Matrix creation, Annotating the Matrix with T/F
			matrix = numpy.zeros((rows,sum_x))
			L_of_constructs = [len(x) for x in constructions]
			#print "tagged words: ",tagged_words
			#print "before: ",matrix
			for i in range(len(matrix)):
				for j in range(len(matrix[0])):
					if tagged_words[i][1] == columnnames[j]:
						matrix[i][j] = 1
		
		
			#print "after: ",matrix


			##################################Call metrics to get best construction as output##########################

			#Calling metric1, returns value for each construction
			m1,words_covered=Mt.metric1(matrix,L_of_constructs)
			#print "Outside metric one", m1
			#print "metric1: ",m1
			c=0
			confidence=[[] for x in range(len(constructions))]
			quality=[[] for x in range(len(constructions))]
			done_length = 0
			for cons in constructions:
				#print cons
				m2=0
				s = []
				for k in cons:
					for sc in specificities_of_cons:
						if k in sc[0]:
							s.append(sc[1])
				#print "cons to m3: ", cons, "sp to m3: ", s
				m3=(Mt.metric3(cons, s))

				#print "Outside metric three", m3
				#print "metric 3 ",m3
	
				words_in_cons=[]
				done_length = done_length + L_of_constructs[c]
				sub_matrix = matrix[:, done_length-L_of_constructs[c] : done_length]
				for w in range(len(sub_matrix)):
					count=0
					for k in range(len(sub_matrix[0])):
						if sub_matrix[w][k]==1:
							if count==0:
								count=1

								words_in_cons.append(words[w])
							else:
								pass
		
				#print "words_in_cons: ",words_in_cons		
		
				t=time.time()
				#print "Before m4 time: ",t
				#print "words_in_cons: ", words_in_cons, "cons: ", cons
				s = []
				for k in words_in_cons:
					for sw in specificities_of_words:
						if k in sw[0]:
							s.append(sw[1])

				m4=(Mt.metric4(s,cons))
				#print "outside metric four", m4
				#print "After m4: ",m4," time: ",time.time()-t
				#m4=1.6			
				#print "m1: ",m1[c]," m2: ",m2," m3: ",m3," m4: ",m4
				max_m=sorted([m1[c],m2,m3,m4],key=float)

				confidence[c].append(Mt.confidence(max_m)) 
				#print "words covered: ",words_covered[c]," confidence: ",confidence[c][0]," total words: ",rows
				quality[c].append(Mt.quality(confidence[c][0],float(words_covered[c]),float(rows)))
				#print "Quality ",Mt.quality(confidence[c][0],float(words_covered[c]),float(rows))
				c+=1

			max_q=-2
			quality_index=0
			for x in range(len(quality)):
				if quality[x]>max_q:
					max_q=quality[x]
					max_c=confidence[x]
					quality_index=x

				else:
					pass			


			#Finding tagged words for the returned construction
			final_words=[]
			for r in tagged_words:
				for c in constructions[quality_index]:
					if r[1]==c:
						final_words.append(r[0])


			#print "Construction with maximum confidence(",max_c,") is: ",constructions[quality_index]

			#print "Best construction with quality(",max_q,") is: ",constructions[quality_index]," and the tagged words are ",final_words	
			F.append(cnet.main_conceptnet(final_words))	
			#print "Output: ",zip([str(constructions[quality_index])],max_c,max_q), F
			output.append(zip([str(constructions[quality_index])],max_c,max_q))
			end_time = time.time()
			#print("Elapsed time was %g seconds" % (end_time - start_time))

		else:
			#print "In pass"
			pass


	
except Exception as e:
	pass

	
finally:

	#Inserting all the parsed data from cogparse and conceptnet vector in json		

	f=open('conceptnet_vector.json','w')
	d=json.dump(F,f,indent=2)
	f.close()
	f=open("cogparsed_reviews.json",'w')
	d=json.dump(output,f,indent=2)
	f.close()

