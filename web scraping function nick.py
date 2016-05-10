# -*- coding: utf-8 -*-

# Import modules
from bs4 import BeautifulSoup
import urllib2
import time, random
import json
import os


'''

 Input: URL of restaurant
 Output: JSON file with 

 To scrape a webpage, the function getData scrapes the site, and the function createJSON writes the data in a file. 
 Elements in JSON:
 - Review
 - Rating
 - User name
 - User Location
 - Number of friends of user
 - Number of reviews the user wrote
 - Restaurant name
 - Ranking of the review in restaurant
 - Type of restaurant (list)
 - Price category (Number of €€€€ in restaurant page)
 
'''



# Create functions

def getReview(soup):
    res=soup.select(".review-content p")
    reviews=[review.text for review in res]
    return reviews

def getStars(soup):
    res=soup.select("[itemprop~=ratingValue]")
    stars=[star['content'] for star in res]
    del stars[0]
    return stars


def getUserName(soup):
    res=soup.select("[itemprop~=author]")
    users=[user['content'] for user in res]
    return users

def getUserLocation(soup):
    res=soup.select(".responsive-hidden-small b")
    location=[loc.text for loc in res]
    return location

def getNumFriends(soup):
    res=soup.select(".i-18x18_friends_c-common_sprite-wrap")
    friends=map(lambda x: (x.text.split(" ")[1]), res)
    return friends

def getNumReviews(soup):
    res=soup.select(".i-18x18_review_c-common_sprite-wrap")
    num_reviews=map(lambda x: (x.text.split(" ")[1]), res)
    return num_reviews


def getType(soup):
    res=soup.select(".category-str-list a")
    types=map(lambda x: (str(x.text)), res)
    return types


def getPrice(soup):
    res=soup.select(".bullet-after .price-range")
    types=map(lambda x: (len(x.text)), res)
    return types




def getData(url):
    
    # Get html code
    url = 'http://' + url
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    # Get all the pages with reviews
    pages=soup.select(".page-of-pages")[0].text
    num=str(pages)
    num=filter(str.isdigit, num)[-1]
    num=int(num)
    index=range(20,num*20,20)
    urls=[url + "?start=" + str(sufix) for sufix in index]
    urls.insert(0,url)
    # Characteristics of the restaurant
    # Type of restaurant
    types=getType(soup)
    # Price of restaurant (number of €)
    price=getPrice(soup)
    # Initialize list
    ALL_REVIEWS=[]
    ALL_STARS=[]
    ALL_USER_NAME=[]
    ALL_USER_LOCATION=[]
    ALL_NUM_FRIENDS=[]
    ALL_NUM_REVIEWS=[]
    for link in urls:
        # Get soup
        html = urllib2.urlopen(link).read()
        soup = BeautifulSoup(html, "html.parser")
        # Review
        new_reviews=getReview(soup)
        ALL_REVIEWS=ALL_REVIEWS + new_reviews
        # Stars
        new_stars=getStars(soup)
        ALL_STARS=ALL_STARS + new_stars
        # User Names
        new_names=getUserName(soup)
        ALL_USER_NAME=ALL_USER_NAME + new_names
         # User Location
        new_location=getUserLocation(soup)
        ALL_USER_LOCATION=ALL_USER_LOCATION + new_location
        # Number of Friends
        new_friends=getNumFriends(soup)
        ALL_NUM_FRIENDS=ALL_NUM_FRIENDS + new_friends
        # Number of Reviews
        new_num_reviews=getNumReviews(soup)
        ALL_NUM_REVIEWS=ALL_NUM_REVIEWS + new_num_reviews
        # Sleeping time
        delay = random.randint(1,2)
        time.sleep(delay)
    # Combine all lists
    data = zip(ALL_REVIEWS, ALL_STARS, ALL_USER_NAME, ALL_USER_LOCATION, ALL_NUM_FRIENDS, ALL_NUM_REVIEWS)
    return data, types, price
    
    
#Create JSON: the name of the file is the name of the restaurant

def createJSON(data,url):  
 rest_name=url.split("/")[-1]
 for i in range(len(data)):
     file_name=rest_name+"_"+str(i)+".json"
     out_file = open(file_name,"w")
     doc = list(data[i])
     doc.append(rest_name)
     doc.append(i+1)
     doc.append(tuple(types))
     if len(price)>0: 
     	doc.append(int(str(price[0])))
     json_str = json.dumps(doc, indent = 4)
     out_file.write(json_str)
     out_file.close()


with open("/Users/Nick/Desktop/Text-Mining/accepted_yelp_links", "r") as fi:
    links = json.load(fi)

#0-300 Nick
#300-500 Yaro
#500-len(links)-1 Aina

for url in links[50:100]:#(len(links)-1)]:
    delay = random.randint(1,5)
    time.sleep(delay)
    try:
        os.chdir("/Users/Nick/Desktop/Links")
        data, types, price=getData(url)        
        createJSON(data, url)
        
    except:
        os.chdir("/Users/Nick/Desktop/Rejected")
        with open("rejected.txt", "a") as f:
            f.write(url)
            f.write("\n")
