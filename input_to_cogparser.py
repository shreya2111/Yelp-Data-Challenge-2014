import os
import json
import nltk
import re
from nltk.tag.stanford import POSTagger
from nltk import CFG
from nltk.tree import Tree
from collections import defaultdict

# This python script generates the initial constructions
# for a set of text in a JSON file. Input is: the JSON file should
# have reviews of a particular restaurant.


######################################
########## FUNCTION BEGINS ###########
######################################
def initialise_const(inputtext):

    tag_dict = defaultdict(list)

    #posTagger
    posTagger=POSTagger('stanford-postagger/models/english-bidirectional-distsim.tagger','stanford-postagger/stanford-postagger.jar')
    tagged_sent=posTagger.tag(inputtext.split())
    # print tagged_sent

    # Put tags and words into the dictionary
    for word, tag in tagged_sent:
        if tag not in tag_dict:
            tag_dict[tag].append(word)
        elif word not in tag_dict.get(tag):
            tag_dict[tag].append(word)

    output = ""
    nouns = ""
    det = ""
    verbs = ""
    pr = ""
    np = ""
    propn = ""
    adj = ""
    to = ""
    adv = ""

    for tag, words in tag_dict.items():
        for word in words:
                if tag == 'NNS' or tag == 'NN' or tag == 'N' or tag == 'WP':
                	nouns = nouns + "| \'" + word + "\'"
                if tag == 'VBG' or tag == 'VBN' or tag == 'VBD' or tag == 'VBP' or tag == 'VBZ' or tag == 'VB' or tag == 'V':
                	verbs = verbs + "| \'" + word + "\'"
                if tag == 'DT' or tag == 'Det' or tag == 'PRP$' or tag == 'WDT':
                	det = det + "| \'" + word + "\'"
                if  tag == 'CC' or tag == 'P' or tag == 'IN':
                	pr = pr + "| \'" + word + "\'"
                if tag == 'PRP':
                	np = np + "| \'" + word + "\'"
                if tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
                	adj = adj + "| \'" + word + "\'"
                if tag == 'NNP' or tag == 'NNPS':
                	propn = propn + "| \'" + word + "\'"
                if tag == 'TO':
                	to = to + "| \'" + word + "\'"
                if tag == 'RB':
                	adv = adv + "| \'" + word + "\'"

    if nouns != "":
    	nouns = nouns.split()
    	nouns.pop(0)
    	nouns = "".join(nouns)


    if verbs != "":
    	verbs = verbs.split()
    	verbs.pop(0)
    	verbs = "".join(verbs)


    if det != "":
    	det = det.split()
    	det.pop(0)
    	det = "".join(det)

    if pr != "":
    	pr = pr.split()
    	pr.pop(0)
    	pr = "".join(pr)

    if adj != "":
    	adj = adj.split()
    	adj.pop(0)
    	adj = "".join(adj)

    if to != "":
    	to = to.split()
    	to.pop(0)
    	to = "".join(to)

    if adv != "":
    	adv = adv.split()
    	adv.pop(0)
    	adv = "".join(adv)
    if np != "":
        np = np.split()
        np.pop(0)
        np = "".join(np)

    #### GENERATING OUR OWN GRAMMAR ######
    grammar = """S -> NP VP | NP VP DESC
    PP -> P NP
    NP -> Det N | Det N PP | Det Adj N | Adj N | TO N | PropN | PREPS | Det PropN
    DESC -> Adj
    PREPS -> """ + np + """
    PropN -> """ + propn + """
    VP -> V NP | VP PP | TO V | ADV V | V V | TO V | V TO | VP ADV
    Det -> """ + det + """
    Adj -> """ + adj + """
    N -> """ + nouns + """
    P -> """ + pr + """
    V -> """ + verbs + """
    TO -> """ + to + """
    ADV -> """ + adv

    #### 'INPUT' IS THE FINAL ARRAY TO BE RETURNED #####
    INPUT = [['agent'],['action'],['object'],['loc'],['location'],['description']]
    grammar = CFG.fromstring(grammar)
    parser = nltk.ChartParser(grammar)
    flag = 0
    try:
        trees = parser.parse(inputtext.split())
        flag = 1
    except ValueError as e:
        ## If there is a problem with the parsing, return the INPUT string to main function as it is.
        return INPUT, inputtext
    if flag == 1:
        ## If no problem with parsing, do the following
        TREE = list()
        i = 0
        for tree in trees:

            TREE = tree
            i = i+1
        ## Take the LAST tree returned.

        try:
            L_of_NP = len(TREE[0])
            NP = TREE[0]
        except:
            L_of_NP = 0
        try:
            L_of_VP = len(TREE[1])
            VP = TREE[1]
        except:
            L_of_VP = 0
        try:
            L_of_DE = len(TREE[2])
            DE = TREE[2]
        except:
            L_of_DE = 0

        NP_sub = []
        VP_sub = []
        DE_sub = []

        for i in range(L_of_NP):
            NP_sub.append(NP[i])

        for i in range(L_of_VP):
            VP_sub.append(VP[i])

        for i in range(L_of_DE):
            DE_sub.append(DE[i])

        agentSlot = []
        actionSlot = []
        locationSlot = []
        objectSlot = []
        descSlot = []
        loc = []
        # Actual parsing of agent, object.. etc begins here.
        for children in NP_sub:
            if children.label() != 'PP':
                for i in range(len(children.leaves())):
                    agentSlot.append(children.leaves()[i])
            if children.label() == 'PP':
                for child in children:
                    preps = 0
                    if child.label() == 'P':
                        for i in range(len(child.leaves())):
                            loc.append(child.leaves()[i])
                            preps = 1
                    if preps != 0:
                        if child.label() == 'N' or child.label() == 'NP':
                            for i in range(len(child.leaves())):
                                locationSlot.append(child.leaves()[i])
                    if preps == 0:
                        if child.label() == 'N' or child.label() == 'NP':
                            for i in range(len(child.leaves())):
                                agentSlot.append(child.leaves()[i])

        strtype = "str"
        for children in VP_sub:
            if children.label() != 'PP':
                for middle in children:
                    if type(middle) != type(TREE):
                        actionSlot.append(middle)
                    else:
                        if middle.label()!='PP':
                            for child in middle:
                                if type(child) == type(TREE):
                                    if child.label() != 'NP':
                                        for i in range(len(child.leaves())):
                                            actionSlot.append(child.leaves()[i])
                                    else:
                                        for i in range(len(child.leaves())):
                                            objectSlot.append(child.leaves()[i])
                                else:
                                    actionSlot.append(child)
                        if middle.label()=='PP':
                            for child in middle:
                                preps = 0
                                if child.label() == 'P':
                                    for i in range(len(child.leaves())):
                                        loc.append(child.leaves()[i])
                                        preps = 1
                                        
                                if preps ==0 :
                                  
                                    if child.label() == 'N' or child.label() == 'NP':
                                        for i in range(len(child.leaves())):
                                            locationSlot.append(child.leaves()[i])
                                if preps != 0 :
                              
                                    if child.label() == 'N' or child.label() == 'NP':
                                        for i in range(len(child.leaves())):
                                            objectSlot.append(child.leaves()[i])
            if children.label() == 'PP':
                for child in children:
                    preps = 0
                    if child.label() == 'P':
                        for i in range(len(child.leaves())):
                            loc.append(child.leaves()[i])
                            preps = 1
                    if preps !=0 :
                        if child.label() == 'N' or child.label() == 'NP':
                            for i in range(len(child.leaves())):
                                locationSlot.append(child.leaves()[i])
                    if preps == 0 :
                        if child.label() == 'N' or child.label() == 'NP':
                            for i in range(len(child.leaves())):
                                objectSlot.append(child.leaves()[i])

        for children in DE_sub:
            if children.label() == 'Adj':
                for i in range(len(children.leaves())):
                    descSlot.append(children.leaves()[i])



        # print "AGENT: ", agentSlot
        # print "ACTION: ", actionSlot
        # print "LOCATION: ", locationSlot
        # print "OBJECT: ", objectSlot
        # print "DESCRIPTION: ", descSlot
        # print "LOC: ", loc

       
        sent = inputtext.split()

        for word in sent:
            if word in agentSlot:
                INPUT[0].append(word)
            if word in actionSlot:
                INPUT[1].append(word)
            if word in objectSlot:
                INPUT[2].append(word)
            if word in loc:
                INPUT[3].append(word)
            if word in locationSlot:
                INPUT[4].append(word)
            if word in descSlot:
                INPUT[5].append(word)

        return INPUT, inputtext
###############################
##### END OF FUNCTION #########
###############################



#################
##### MAIN #####
#################

os.chdir('dataset/')

## FOR ONLY ONE BUSINESS
reviewsfile = open('business_review.json')
data = json.load(reviewsfile)
reviewsfile.close()
CONST = []
number = 0
for index in range(len(data)):
    review = data[index]
    lines = re.split("[\n|.|!|?]", review)
    for line in lines:
        number = number + 1
        print number
        if len(line.split()) <= 6:
            inputtext = line
            final, used_text = initialise_const(inputtext.replace("'", ""))
            CONST.append([final, used_text])
        if len(line.split()) > 6:
            words = line.split()
            L = len(words)
            Q = L/6
            rem = L%6
            for l in range(Q):
                inputtext = ' '.join(words[l*6:(l+1)*6])
                final, used_text = initialise_const(inputtext.replace("'", ""))
                CONST.append([final, used_text])
            inputtext =  ' '.join(words[L-6:L])
            final, used_text = initialise_const(inputtext.replace("'", ""))
            CONST.append([final, used_text])

with open("const_sentences.json", 'w') as outfile:
    json.dump(CONST, outfile, indent=2)
outfile.close()
