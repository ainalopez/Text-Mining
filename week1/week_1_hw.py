# -*- coding: utf-8 -*-
import numpy as np
import codecs
import nltk
import re
from nltk.tokenize import wordpunct_tokenize
from nltk import PorterStemmer
import math
from itertools import repeat


class Corpus():
    
    """ 
    The Corpus class represents a document collection
     
    """
    def __init__(self, doc_data, stopword_file, clean_length):
        """
        Notice that the __init__ method is invoked everytime an object of the class
        is instantiated
        """
        

        #Initialise documents by invoking the appropriate class
        self.docs = [Document(doc[0], doc[1], doc[2]) for doc in doc_data] 
        
        self.N = len(self.docs)
        self.clean_length = clean_length
        
        #get a list of stopwords
        self.create_stopwords(stopword_file, clean_length)
        
        #stopword removal, token cleaning and stemming to docs
        self.clean_docs(2)
        
        #create vocabulary
        self.corpus_tokens()
        
    def clean_docs(self, length):
        """ 
        Applies stopword removal, token cleaning and stemming to docs
        """
        for doc in self.docs:
            doc.token_clean(length)
            doc.stopword_remove(self.stopwords)
            doc.stem()        
    
    def create_stopwords(self, stopword_file, length):
        """
        description: parses a file of stowords, removes words of length 'length' and 
        stems it
        input: length: cutoff length for words
               stopword_file: stopwords file to parse
        """
        
        with codecs.open(stopword_file,'r','utf-8') as f: raw = f.read()
        
        self.stopwords = (np.array([PorterStemmer().stem(word) 
                                    for word in list(raw.splitlines()) if len(word) > length]))
        
     
    def corpus_tokens(self):
        """
        description: create a set of all all tokens or in other words a vocabulary
        """
        
        #initialise an empty set
        self.token_set = set()
        for doc in self.docs:
            self.token_set = self.token_set.union(doc.tokens)

    def document_term_matrix(self):
        """
        description:  returns a D by V array of frequency counts
        """
        # subroutine: computes the counts of each vocabulary in the document
        def counts(doc):
            # initialize a matrix
            term_mat = [0]*len(self.token_set)
            for token in doc.tokens:
                term_mat[list(self.token_set).index(token)] = term_mat[list(self.token_set).index(token)] + 1
            return term_mat;
        
        self.doc_term_matrix = []
        
        for doc in self.docs:
            self.doc_term_matrix.append([doc.pres + " " + doc.year, counts(doc)])

    def tf_idf(self):
        """
        description:  returns a D by V array of tf-idf scores
        """
        # Compute inverse document frequency
        idf = [0]*len(self.token_set)
        for token in self.token_set:
            ind = 0
            for doc in self.docs:
                if token in doc.tokens:
                    ind += 1
                idf[list(self.token_set).index(token)] = math.log(self.N/ind)

        # Create a subroutine that computes tf_idf for one document
        def tfidf(doc):
            term_mat = [0]*len(self.token_set)
            for token in doc.tokens:
                term_mat[list(self.token_set).index(token)] = term_mat[list(self.token_set).index(token)] + 1
            
            for i,term in enumerate(term_mat):
                if term != 0:
                    term_mat[i] = (1 + math.log(term)) * idf[i]
            return term_mat;
    
        #tf_idf
        self.tf_idf_matrix = []
        for doc in self.docs:
            self.tf_idf_matrix.append([doc.pres + " " + doc.year, tfidf(doc)])


    def dict_rank(self, n, dictionary, token_repr):
        """
        description:  returns the top n documents based on a given dictionary and represenation of tokens
        """
        if token_repr == "tf-idf":
            self.tf_idf()
            representation = self.tf_idf_matrix
            
        if token_repr == "doc-term":
            self.document_term_matrix()
            representation = self.doc_term_matrix
            
        # Return top n docs based on dictionary given
        score = []
        x=self.token_set
        x=list(x)
        for token in x: 
            try:
                score.append(dictionary[token])
            except: 
                score.append(0)

        # get a vector with all the scores in order
        score=[int(x) for x in score]
        rank = {}
        elements=range(len(representation))
   
        for i in elements:
            rank[representation[i][0]] = np.dot(score,representation[i][1])
            
        # Get sorted view of the keys.
        s = sorted(rank, key=rank.get, reverse=True)[0:(n-1)]
        
        ranking = {}
        for key in s:
            ranking[key] =  rank[key]
        
        return ranking 




class Document():
    
    """ The Doc class rpresents a class of individul documents
    
    """
    
    def __init__(self, speech_year, speech_pres, speech_text):
        self.year = speech_year
        self.pres = speech_pres
        self.text = speech_text.lower()
        self.tokens = np.array(wordpunct_tokenize(self.text))
        
        
        
    def token_clean(self,length):

        """ 
        description: strip out non-alpha tokens and tokens of length > 'length'
        input: length: cut off length 
        """

        self.tokens = np.array([t for t in self.tokens if (t.isalpha() and len(t) > length)])


    def stopword_remove(self, stopwords):

        """
        description: Remove stopwords from tokens.
        input: stopwords: a suitable list of stopwords
        """

        
        self.tokens = np.array([t for t in self.tokens if t not in stopwords])


    def stem(self):

        """
        description: Stem tokens with Porter Stemmer.
        """
        
        self.tokens = np.array([PorterStemmer().stem(t) for t in self.tokens])


#############################################  QUESTIONS  ###############################################


###################  EXERCISE 1  ###################
# The three methods are added in the class Corpus.



###################  EXERCISE 2  ###################

# In the same folder as this document in Github, there is a pdf with our answers 
# to this question. Below can be found the code. BE CAREFUL!!! IT CAN TAKE A 
# COUPLE OF HOURS

def parse_text(textraw, regex):
    """takes raw string and performs two operations
    1. Breaks text into a list of speech, president and speech
    2. breaks speech into paragraphs
    """
    prs_yr_spch_reg = re.compile(regex, re.MULTILINE|re.DOTALL)
    
    #Each tuple contains the year, last ane of the president and the speech text
    prs_yr_spch = prs_yr_spch_reg.findall(textraw)
    
    #convert immutabe tuple to mutable list
    prs_yr_spch = [list(tup) for tup in prs_yr_spch]
    
    for i in range(len(prs_yr_spch)):
        prs_yr_spch[i][2] = prs_yr_spch[i][2].replace('\n', '')
    
    #sort
    prs_yr_spch.sort()
    
    return(prs_yr_spch)
    
text = open("/Users/ainalopez/Downloads/text_mining-master/data/pres_speech/sou_all copy.txt", 'r').read()
#text = open("/home/yaroslav/Projects/text_mining/data/pres_speech/sou_all.txt", 'r').read()
regex = "_(\d{4}).*?_[a-zA-Z]+.*?_[a-zA-Z]+.*?_([a-zA-Z]+)_\*+(\\n{2}.*?)\\n{3}"
pres_speech_list = parse_text(text, regex)

#Instantite the corpus class
# corpus = Corpus(pres_speech_list, '/home/yaroslav/Projects/text_mining/data/stopwords/stopwords.txt', 2)
corpus = Corpus(pres_speech_list, '/Users/ainalopez/Downloads/text_mining-master-2/data/stopwords/stopwords.txt', 2)

# Import dictionary from excel file
import pandas as pd
#df = pd.read_excel("/home/yaroslav/Dropbox/BGSE/3rd Term/Text Mining/LoughranMcDonald_MasterDictionary_2014.xlsx", skiprows=0)
df = pd.read_excel("/Users/ainalopez/Downloads/dictionary1.xlsx", skiprows=0)
w = df['Word']
words = [str(x).lower() for x in df['Word']]
words=[PorterStemmer().stem(t) for t in words]
score = [str(x).lower() for x in df['Positive']] # or any other method
dictionary=dict(zip(words,score))

# Applying dict_rank function
X1 = corpus.dict_rank(corpus.N, dictionary,"doc-term")
X2 = corpus.dict_rank(corpus.N, dictionary,"tf-idf")

# Print the Ranking 
print sorted(X1, key=X1.get, reverse=True)
print sorted(X2, key=X2.get, reverse=True)    





###################  EXERCISE 3  ################### 


def get_dictionary():
    '''This function opens the AFINN-111 file and converts it
    into a dictionary with words as keys and valence score as values
    Input: None
    Output: Dictionary, Dictionary with words as keys
    and the valence of word as value'''
    
    #open AFINN-111 file as a list
    with open("/Users/Nick/Desktop/AFINN-111.txt", "r") as f:
        lines = f.readlines()

    #split by tab
    content = [line.split("\t") for line in lines]
    
    #create dictionary 
    dictionary = dict((word, int(valence)) for (word,valence) in content)

    return dictionary





###################  EXERCISE 4  ###################
# ANSWER:
# What is the score of the speech you have been assigned?
# Nick Speech: 130, Roosevelt, Year=1943
# Aina Speech: 1071, Taft, Year=1911
# Yaroslav Speech: 266, Polk, Year=1847

# Which year, president gave the least and most positive speech?
# Top score: 1649, Carter, Year=1981
# Bottom score: -6, Harding, Year=1922

# CODE below:

def get_sentiment(word_list):
    '''This function computes the score for a list of words
    Input: word_list, a list of words
    Output: Int, summation of valences for words in word list'''

    #get dictionary
    dictionary = get_dictionary()

    #initialize empty valence list
    valence_list = []

    #loop through word list
    for key in word_list:
        try:
            #if key in dictionary
            valence_list.append(dictionary[key])
   
        except:
            #if not continue
            pass
    return sum(valence_list)

def parse_text(textraw, regex):
    """takes raw string and performs two operations
    1. Breaks text into a list of speech, president and speech
    2. breaks speech into paragraphs
    """
    prs_yr_spch_reg = re.compile(regex, re.MULTILINE|re.DOTALL)
    
    #Each tuple contains the year, last ane of the president and the speech text
    prs_yr_spch = prs_yr_spch_reg.findall(textraw)
    
    #convert immutabe tuple to mutable list
    prs_yr_spch = [list(tup) for tup in prs_yr_spch]
    
    for i in range(len(prs_yr_spch)):
        prs_yr_spch[i][2] = prs_yr_spch[i][2].replace('\n', '')
    
    #sort
    prs_yr_spch.sort()
    
    return(prs_yr_spch)
    
#text = open("/Users/Nick/Desktop/sou_all.txt", 'r').read()
with open("/Users/Nick/Desktop/sou_all.txt", 'r') as f:
    text = f.read()
    
regex = "_(\d{4}).*?_[a-zA-Z]+.*?_[a-zA-Z]+.*?_([a-zA-Z]+)_\*+(\\n{2}.*?)\\n{3}"
pres_speech_list = parse_text(text, regex)

corpus = Corpus(pres_speech_list, '/Users/Nick/Desktop/stopwords.txt', 2)

score = []

for doc in corpus.docs:
    score.append((doc.year, doc.pres, get_sentiment(doc.text.split())))

#sort by score
sort_score = sorted(score, key = lambda tuple:tuple[2], reverse=True)


print sort_score
