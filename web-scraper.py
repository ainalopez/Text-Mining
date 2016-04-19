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

url = 'http://www.yelp.com/search?find_desc=Restaurants&find_loc=barcelona'
open_url = urllib2.urlopen(url).read()

soup = bs(open_url, "html.parser")

#get all restaurant reviews
all_href = [links.get('href') for links in soup.find_all('a')]

all_links = [link for link in all_href if "/biz" in link]

