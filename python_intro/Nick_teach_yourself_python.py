# 1 use open a connection to the file
# 2 read contents of the file
# 3 use the json module to read the string as a list
#(replace None with relevant code)

import json
import re

file_handle = open("1943_Roosevelt_Nick.txt")
file_content = file_handle.read()
file_handle.close()
speech = json.loads(file_content)

#Notice that type(speech) is list. Please take a moment to go through
#the python list documentation and check out the various ways to manipulate
#lists.

#2 The first element of the list is the year of speech, the second element is
#the president who gave it, while the third is the transcript of the same.
#Inspect the transcript. Note the commonly used non-alphanumerical characters.
#Use an appropriate method of strings to get rid of them.
#Use an appropriate string method to split the string of the speech into a list
#of smaller list of words.
#Convert all words into lower case and return the list. Use a for loop. Then
#use a list comprehension to do the same.

#1
stripped_text = re.sub(r'[\W_]', ' ', speech[2])
stripped_text = str(stripped_text)

#2
word_list = stripped_text.split()

#3 
#Convert to lower case using for loop
lower_words = []
for word in word_list:
    low = word.lower()
    lower_words.append(low)

#Convert to lower case using list comprehension
lower_words_list = [word.lower() for word in word_list]

#####3#####
#Create a function _preprocess_ that takes as arguments _text_ and
#_non_alphanum_, a string of non-alphanumeric characters that you want get
#rid of. Perform all operations specfied in the previous question.
#However, converting to lowercase should be an optional argument. The data
#structure returned should be a list of words.

def preprocess(text, alphanum_chars, lower = True):
    
    #remove user given characters
    
    alpha = str([alphanum_chars])
    stripped_text = re.sub(alpha, ' ', text)
    stripped_text = str(stripped_text)

    #split string into list of smaller list of words
    
    word_list = stripped_text.split()

    #convert to lower case
    
    if lower:
        lower_words = [word.lower() for word in word_list]
        return lower_words
    
    return word_list
    
####4####
#Create a function _word_freq_ that takes as input a word list that has
#been preprocessed and returns a dictionary of the word frequency. Which
#is the fourth most frequent word of your word list? (Provide code that
#computes it)

def word_freq(word_list):
    
    #count frequencies
    
    freq = [word_list.count(word) for word in word_list]

    #create list of tuples and sort by second value in tuple
    
    sort = sorted(zip(word_list, freq), key = lambda tuple:tuple[1], reverse=True)

    return dict(sort)


#Get 4th most frequent word
print list(word_freq(word_list))[3]

####5####
#Write a function that takes as input a word list and returns a dictionary of
#the frequencies of word lengths. Do not use the api collections for this
#assignment. But have a look at its [documentation](https://docs.python.org/2/library/collections.html).
#Its useful tool to have in your repository.

def word_lengths(word_list):
    #count length of words
    
    lengths = [len(word) for word in word_list]

    #count frequency of word lengths

    frequency = [lengths.count(freq) for freq in lengths]

    #create list of tuples (length of word, frequency)

    freq = zip(lengths, frequency)
    
    return dict(freq)


###6###
#Load the file _sou_all.txt_ in ./data/pres_speech. Inspect its contents.
#Familiarise yourself with using regular expressions in python. You can use this
#[document](https://docs.python.org/2/howto/regex.html) as a starting point.
#Now use regular expressions to seperate the different speeches. Your function
#should accept the text and a regular expression as input and return a list of
#lists. Each element of the list should be a list with following structure:

#[[year],[president],[paragraph1,paragraph2,...]]
#1. year
#2. president
#3. List of the transcript of the speech broken down into paragraphs.

#Save your result as json

file_handle = open("sou_all.txt","r")
content = file_handle.read()
file_handle.close()

def pres_speech(text, reg_express="Unused"):
    
    #split by paragraphs
    paragraphs = re.split(r"\n\n", text)
    
    list_append = []
    paragraph_append = []

    #loop through paragraphs
    for paragraph in paragraphs:

        #if paragraph contains president name and year (starts with two stars)
        if "**" in paragraph:
            
            #remove stars from president name
            replace = paragraph.strip('*')
            
            #remove underscore
            replace = replace.split('_')
            
            #gives list of year
            year = [replace[1]]
            
            #list of president name
            prez = [replace[3]+' '+replace[4]]

            #append year and president (as lists) to empty list
            list_append.append(year)
            list_append.append(prez)
            
        else:
            #append president speech (as list) to empty list
            paragraph_append.append(paragraph)
            paragraph_append = [','.join(paragraph_append)]
            
    list_append.append(paragraph_append)

    with open("speech.json", "w") as outfile:
        json.dump(list_append, outfile)
        
    return list_append
