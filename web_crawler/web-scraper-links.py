# for establishing a connection between python and website
import urllib2

# for retreiving information from websites 
from bs4 import BeautifulSoup as bs

#convert xml as string to an ordered dictionary 
import xmltodict

# to read arguments from command line
import os 

#Get numpy arrays
#import numpy as np

#To read the folder structure of the target
import sys

#to add randomised waiting time
import time, random

import json

def write_json(file_name, data):
    '''This function writes a json file
    Input: file_name, str, name of the file to write,
    data, list, list of data to write
    Output: None'''
    
    out_file = open(file_name, "w")
    json_str = json.dumps(data, indent = 2)
    out_file.write(json_str)
    out_file.close()
    

yelp = 'www.yelp.com'
res_link = 'http://www.yelp.com/search?find_desc=Restaurants&find_loc=barcelona&start='

start_link = [res_link + str(num) for num in range(0,991,10)]

links_list = []
denied_links = []

for url in start_link:
    
    delay = random.randint(1,2)
    #pause execution for 1-2 seconds
    time.sleep(delay)
    
    try:
        #read in html as string
        open_url = urllib2.urlopen(url).read()

        #parse html
        soup = bs(open_url, "html.parser")

        #get all restaurant reviews
        all_href = [links.get('href') for links in soup.find_all('a')]
        all_href_str = [str(links) for links in all_href]
        all_links = [yelp + link for link in all_href_str
                     if "/biz/" in link and "?" not in link and "%" not in link]
        
        #eliminate duplicates
        links_dup = list(set(all_links))
        links_list.append(links_dup)

    except:
        denied_links.append(url)

#write accepted links
write_json("accepted_yelp_links", links_list)

#write denied links
write_json("denied_yelp_links", denied_links)
