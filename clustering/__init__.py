#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from hashlib import md5
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

#import feedparser
import nltk
#from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english')
#import time
import feedparser
import time
import mimetypes
from bs4 import BeautifulSoup
import re, math
import ast
from collections import Counter

from django.conf import settings
from django.contrib.sites.models import Site

from tagging.models import Tag

from planet.models import (Blog, Generator, Feed, FeedLink, Post, PostLink,
        Author, PostAuthorData, Enclosure, Category, Cluster)
from planet.signals import post_created

class PostAlreadyExists(Exception):
    pass

def get_cosine(vec1, vec2):
     
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])
     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator
#WORD = re.compile(r'\w+')
#c=Cluster.objects.get(id=1)
def process_feed(feed_url, create=False, category_title=None):
    """
    Stores a feed, its related data, its entries and their related data.
    If create=True then it creates the feed, otherwise it only stores new
    entries  and their related data.
    """

                    #CREATE THE VECTOR FIELD MYVECTOR HERE
		    WORD = re.compile(r'\w+')	
                    soup = BeautifulSoup(content)
                    combo=[] # desc and title
                    words= nltk.wordpunct_tokenize(soup.get_text())
                    titlez = nltk.wordpunct_tokenize(title)
                    words.extend(titlez)
                    for word in words:
                        if word in stopwords.words('english'): 
                        	words.remove(word) 
                    for word in words:
                        combo.append(stemmer.stem(word))
                
                    lowerwords=[x.lower() for x in combo if len(x) > 1]

                    def text_to_vector(text):
                        words = WORD.findall(text.lower())
                        return Counter(words)
                    # Making vectors                    
                    vector=text_to_vector(str(lowerwords))      
                    del vector['u']
		    vec33=str(vector)
		    vec=vec33.replace("Counter","")
		    print(vec)
		    c=Cluster.objects.get(id=1)
		    clus_id=c.cluster_id
		    i=0
		    rank=1
		    for posts in Post.objects.all():
			threshold=0
			if posts.feed!=planet_feed:
				#vec11=posts.myvector.replace("Counter","")
				#vec22=vector.replace("Counter","")
				vec1=ast.literal_eval(posts.myvector)
				vec2=ast.literal_eval(vec)
				threshold=get_cosine(vec1,vec2)
			if threshold>0.28:
				#matchposts[i]=posts
				posts.rank+=1
				posts.save()  
				i+=1
				clus_id=posts.cluster_id
		    if i==0:
			c.cluster_id+=1
			c.save()
			clus_id=c.cluster_id
			rank=1
		    elif i>0:
			rank=i

                    post = Post(title=title, url=url, guid=guid, content=content,
                        comments_url=comments_url, image_url=image_url,date_modified=date_modified,
                        feed=planet_feed,cluster_id=clus_id,rank=rank,myvector=vec,category=category)
                    
                    # To have the feed entry in the pre_save signal
                    post.entry = entry
                    post.save()


				

   
