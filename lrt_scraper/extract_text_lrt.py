# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 08:10:55 2021

@author: user2
"""
import pandas as pd
import ast
import time, urllib
from urllib.request import urlopen

import requests

import csv
import pandas
import re
import os
from pathlib import Path

from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



col_names = ['title', 'text', 'summary', 'category']
df  = pandas.DataFrame(columns = col_names)

path = r'C:\Users\user2\git\python\NN\lrt scraper\data\New folder'
files = os.listdir(path)

offset = 1816

for file in files:
    with open('C:/Users/user2/git/python/NN/lrt scraper/data/New folder/'+file,'r') as f:
        my_set = ast.literal_eval(f.read())
        links= list(my_set)
    ## Create empty file
    col_names = ['title', 'text', 'summary', 'category']
    df  = pandas.DataFrame(columns = col_names)
    
    file_pth = Path('C:/Users/user2/git/python/NN/lrt scraper/lrt_articles/lrt-%s.csv' % (file.split(".")[0]))# path to check if file exist
    if not file_pth.exists():
        df.to_csv(file_pth, header=col_names, sep='\t')
        offset=0
    
    for j,link in enumerate(links[offset:]):
        tmp_df = pandas.DataFrame(columns = col_names)
        
        print('{}/{} \t{}'.format(offset, len(links), file.split(".")[0]))
        res =urlopen('https://www.lrt.lt' + link) # open article
        soup = BeautifulSoup(res.read(), 'html.parser')
        try:
            title = soup.find(class_="title-block__heading").text.strip() # get article title
        except:
            title = 'Nera pavadinimo'
            print("Nera pavadinimo!")
        try:
            summary = soup.find(class_='text-lead').text.strip() # get article summary
        except:
            summary = 'Nera summary'
            print('Nera summary')
        
        text = ''
        try:
            for el in soup.select("p")[1:]: # get article text
                text += el.text.strip()
        except:
            text = 'Nera teksto'
            print(text)
            
        tmp_df = tmp_df.append({'text' : text , 'summary' : summary, 'title' : title, 'category' : file.split(".")[0]}, ignore_index=True) # add to data frame
        
        tmp_df.to_csv(file_pth, header=False, sep='\t', mode='a')
        offset+=1

        # df = df.append({'text' : text , 'summary' : summary, 'title' : title, 'category' : file.split(".")[0]}, ignore_index=True) # add to data frame
    
    # Save
    # df.to_csv('C:/Users/user2/git/python/NN/lrt scraper/lrt_articles/lrt-%s.csv' % (file.split(".")[0]), sep='\t')
    
    
# test_read = pd.read_csv('C:/Users/user2/git/python/NN/lrt scraper/lrt_articles/lrt-lietuvoje.csv', sep='\t')



