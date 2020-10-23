# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:28:45 2020

@author: rsele
"""

# importing libaries
import urllib
from urllib import request, response, error, parse
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# define parameters for url
job_title = "Data Scientist"
location = "Leipzig"
radius = 50 # km around the location
days = 30 # days since posting
limit = 50 # limits the results per page
employment ="fulltime"

params = {'q' : job_title, 'l' : location, 'radius' : radius, 'fromage' : days,
          "jt": employment,"limit":limit}

url = ("https://de.indeed.com/Jobs?" + urllib.parse.urlencode(params))

#create lists to save results
jobs=[]
companies=[]
location=[]
links=[]

#connect to the url
page = requests.get(url)
content = requests.get(url)
soup = BeautifulSoup(content.content, "html.parser")

#get the needed content
jobtitle = soup.find_all("h2",class_="title")
companyname = soup.find_all("span",class_="company")
link = soup.find_all("a",class_="jobtitle turnstileLink")

# iterate through elements on page
for job in jobtitle:
    title = job.a.text
    title= re.sub("\n", "", title)
    jobs.append(title)
    
      
for company in companyname:
    name= company.text
    name= re.sub("\n", "", name)
    
    companies.append(name)
    
  
for ref in link:
    reflink="https://de.indeed.com"+ref.get("href")
    links.append(reflink)    
    
# create the dataframe          
# a few jobs on the resultpage are sponsored 
# these jobs are build in different -> they wont be displayed in the dataframe
joblist = pd.DataFrame()
joblist["Jobs"] = jobs
joblist["Company"]=companies
joblist["Links"]=links

# save the file as excel sheet
joblist.to_excel(r"C:\Users\...",
                 index=False)
