#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install selenium')


# In[3]:


#Author- Rohit Ghumare
#GSC Internship
 
import sys
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# open firefox
browser = webdriver.Firefox()
# navigate to amazon
browser.get("http://www.amazon.in")
 
# find search box and send query
searchField = browser.find_element_by_id("twotabsearchtextbox")
searchField.send_keys(sys.argv[1])
#find search button and click it
submit = browser.find_element_by_class_name("nav-input")
submit.click()
 
#scrape the page for products
url = browser.current_url
result = requests.get(url)
print('Response '+str(result.status_code))
src = result.content
soup = BeautifulSoup(src, 'lxml')
links = []
li = soup.find_all('li')
for x in li:
    links = li.find_all('a')
    for i in links:
        links.append(i['href'])
prices = []
pricess = soup.find_all("span", {"class": "a-price"})
for i in pricess:
    spans = i.find_all('span')
    for span in spans:
        prices.append(span.contents)
 
# write scraping output to file
with open("output.csv", "w") as outfile:
    writer = csv.writer(outfile, escapechar=' ', quoting=csv.QUOTE_NONE)
    writer.writerow(["Product", "Price"])
    writer.writerow([links, prices])


# In[ ]:




