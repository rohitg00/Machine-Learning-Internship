#!/usr/bin/env python
# coding: utf-8

# In[1]:


amazon="https://www.amazon.in/Redmi-Note-Pro-Gold-Storage/product-reviews/B07BJZJWBK/ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews"


# In[2]:


product="Redmi Note 5 Pro (Gold, 64 GB)"


# In[37]:


get_ipython().system('pip install BeautifulSoup4')
get_ipython().system('pip install wordCloud')


# In[38]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re 

import matplotlib.pyplot as plt
from wordcloud import WordCloud


# In[5]:


page = urllib.request.urlopen(amazon)


# In[6]:


soup = BeautifulSoup(page) # body at line 183
# 1302 and 1190 1st review by Sriniketan and review on 1303 <span data-hook="review-body" <div class="a-row a-spacing-small review-data">


# In[7]:


body =soup.body


# In[8]:


reviews=[]


# In[9]:


for i in body.find_all('div',class_="a-row a-spacing-small review-data"):
  print (i.text)
  print("\n")
  reviews.append(i.text)


# In[10]:


reviews #need to remove '\n' from the reviews


# In[11]:


for i in body.find_all('div',class_="a-text-center celwidget a-text-base"):
  p=i.get('li')


# In[12]:


print(p)


# In[13]:


type(p)


# In[14]:


for i in body.find_all('div',class_="a-text-center celwidget a-text-base"):
  #print (i)
  for j in i.find_all('a'):
    print (j.get('href'))
    nextpage=j.get('href')
  print("\n")


# In[15]:


link="https://www.amazon.in"+nextpage
page2 = urllib.request.urlopen(link)
soup = BeautifulSoup(page2)
body =soup.body

for i in body.find_all('div',class_="a-row a-spacing-small review-data"):
  print (i.text)
  print("\n")


# In[16]:


for i in body.find_all('div',class_="a-text-center celwidget a-text-base"):
  print (i)
  for j in i.find_all('a'):
    #print (j.get('href'))
    nextpage=j.get('href')
  next_page=nextpage
  print(next_page)


# In[17]:


for i in body.find_all('div',class_="a-text-center celwidget a-text-base"):
  for j in i.find_all('li',class_="a-last"):
    print(j)


# In[21]:


response = requests.get(amazon)
soup = BeautifulSoup(response.content,"html.parser")# creating soup object to iterate over the extracted content 
reviews = soup.findAll("span",attrs={"class","a-size-base review-text review-text-content"})# Extracting the content under specific tags  


# In[24]:


ip=[]
redmi_reviews=[]
for j in range(len(reviews)):
    ip.append(reviews[j].text)  
    redmi_reviews=redmi_reviews+ip  # adding the reviews of one page to empty list which in future contains all the reviews


# In[25]:


with open("redmi.csv","w",encoding='utf8') as output:
    output.write(str(redmi_reviews))


# In[29]:


import os
os.getcwd()

# Joinining all the reviews into single paragraph 
ip_rev_string = " ".join(redmi_reviews)

import nltk
from nltk.corpus import stopwords


# In[31]:



# Removing unwanted symbols incase if exists
ip_rev_string = re.sub("[^A-Za-z" "]+"," ",ip_rev_string).lower()
ip_rev_string = re.sub("[0-9" "]+"," ",ip_rev_string)


# In[32]:


ip_reviews_words = ip_rev_string.split(" ")

#TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer=TfidfVectorizer(ip_reviews_words,use_idf=True,ngram_range=(1, 3))
X=vectorizer.fit_transform(ip_reviews_words)


# In[33]:


with open("redmi.csv","r") as sw:
    stopwords = sw.read()

stopwords = stopwords.split("\n")


# In[34]:


stopwords.extend(["redmi","mobile","ios","apple","phone","amazon","good","xr","product","great","camera","price"])
ip_reviews_words = [w for w in ip_reviews_words if not w in stopwords]


# Joinining all the reviews into single paragraph 
ip_rev_string = " ".join(ip_reviews_words)


# In[45]:


# WordCloud can be performed on the string inputs. That is the reason we have combined 
# entire reviews into single paragraph
# Simple word cloud


wordcloud_ip = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_rev_string)

plt.imshow(wordcloud_ip)

# positive words # Choose the path for +ve words stored in system
with open("E:\Data science\Python for data science amd AI\positive-words.txt","r") as pos:
    poswords = pos.read().split("\n")
  
poswords = poswords[36:]


# In[47]:


# negative words  Choose path for -ve words stored in system
with open("E:\Data science\Python for data science amd AI\negative-words.txt","r") as neg:
    negwords = neg.read().split("\n")

negwords = negwords[37:]

# negative word cloud
# Choosing the only words which are present in negwords
ip_neg_in_neg = " ".join ([w for w in ip_reviews_words if w in negwords])

wordcloud_neg_in_neg = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_neg_in_neg)

plt.imshow(wordcloud_neg_in_neg)


# In[48]:


# Positive word cloud
# Choosing the only words which are present in positive words
ip_pos_in_pos = " ".join ([w for w in ip_reviews_words if w in poswords])
wordcloud_pos_in_pos = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_pos_in_pos)

plt.imshow(wordcloud_pos_in_pos)


# In[49]:


with open("output.csv", "w") as outfile:
    writer = csv.writer(outfile, escapechar=' ', quoting=csv.QUOTE_NONE)
    writer.writerow(["Product", "Price","Good Reviews"])
    writer.writerow([links, prices, poswords])


# In[ ]:




