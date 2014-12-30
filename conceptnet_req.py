import requests
import json
import inflect
#import Main as cogparser

def concept(word):

	#word=['dog','eats']


	p=inflect.engine()
	user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0'
	headers={'User-Agent': user_agent} 

	url="http://conceptnet5.media.mit.edu/data/5.2/search?"

	#rel='rel=/r/PartOf&'
	#end='end=/c/en/car&'
	#text='text='+word+'&'
	for i in range(len(word)):

		if p.singular_noun(word[i]):
			word[i]=p.singular_noun(word[i])
		else:
			pass

	
	start='start=/c/en/'+word[0]+'&'
	end='end=/c/en/'+word[1]+'&'	
	limit='limit=30'
	search=url+start+end+limit
	#print search
	r = requests.get(search,headers=headers)

	data=r.json()
	
	F=[[] for x in range(2)]
	
	d=[]
	b=0
	if len(data["edges"])>=10:
		b+=1
		F[0].append(word)
		for i in range(10):
				d.append(data["edges"][i]["weight"])
		F[1].append(d)	
	
	return F,b


def main_conceptnet(words):
	#get construction from Main.py
	#Sample words=["apple","tastes","so","good"]
	#print "In main conceptnet"
	F=[]
	for i in range(len(words)):
		if i==len(words)-1:
			G,b=concept([words[0],words[i]])
			if b!=0:
		
				F.append(G) 
		else:

			G,b=concept([words[i],words[i+1]])
			if b!=0:
				F.append(G) 	


	return F

