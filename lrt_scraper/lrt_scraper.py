# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:57:14 2021

@author: user2
"""
import time, urllib
from urllib.request import urlopen

import requests

import pandas
import re

col_names = ['title', 'text', 'summary', 'author']
df  = pandas.DataFrame(columns = col_names)

# url = 'https://www.lrt.lt'
# response = urlopen(url)
# html = response.read()

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.webdriver.chrome.options import Options


temos = ['/naujienos/lietuvoje', '/naujienos/verslas', '/naujienos/lrt-tyrimai', '/naujienos/pasaulyje', '/naujienos/sveikata', '/naujienos/eismas', '/naujienos/sportas', '/naujienos/mokslas-ir-it', '/naujienos/kultura', '/naujienos/veidai', '/naujienos/muzika', '/naujienos/gyvenimas', '/naujienos/tavo-lrt']


#clean data frame
df = pandas.DataFrame(columns = col_names)
df


# driver = webdriver.Chrome(executable_path='C:/Users/user2/git/python/NN/lrt scraper/chromedriver.exe')
# driver.get('https://www.lrt.lt' + tema)

# while True:
#     try:
#         showmore=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH ,'//*[@id="page-content"]/section[2]/a')))
#         showmore.click()
#         # print("page is ready!")
#     except TimeoutException:
#         break
#     except StaleElementReferenceException:
#         break


session = requests.Session()

offset = 4

for (i, tema) in enumerate(temos[offset:]):
    straipsniai = set()
    print(tema)
    # responseTry = urlopen('https://www.lrt.lt' + tema)
    # soup = BeautifulSoup(responseTry.read(), 'html.parser')
    # r = session.get('https://www.lrt.lt'+tema)
    # soup=BeautifulSoup(r.html.html,'html.parser')


    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(executable_path='C:/Users/user2/git/python/NN/lrt scraper/chromedriver.exe', chrome_options=chrome_options)
    driver.get('https://www.lrt.lt' + tema)
    
    def getPageStraipsnius(soup):
        for el in soup.select('h3 a'):
            # print(el.get('href'))
            straipsniai.update([el.get('href')])
    
    k=0
    tmp_len = 0
# Load more pages
    while True:
        print(k, '\t', tema)
        try:
            button = driver.find_element_by_xpath('//*[@id="page-content"]/section[2]/a')
            driver.execute_script("arguments[0].click();", button)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source)
            k+=1
            if k%10 == 0:
                # print("### EXTRACTING ###")
                getPageStraipsnius(soup) # extract links
                print("IS VISO STRAIPSNIU: ", len(straipsniai))
                # SAVE
                with open(r'C:\Users\user2\git\python\NN\lrt scraper\links_'+str(offset)+'.txt','w') as f:
                    f.write(str(straipsniai))
                
                if len(straipsniai) > 20000:
                    break
                elif tmp_len == len(straipsniai):
                    break
                tmp_len = len(straipsniai)
        except TimeoutException:
            break
        except StaleElementReferenceException:
            break

    getPageStraipsnius(soup)
    i+=1
    offset+=1
    
# # LOAD
# import ast
# with open('C:\Users\user2\git\python\NN\lrt scraper\links.txt','r') as f:
#    my_set = ast.literal_eval(f.read())




#     for (a,straipsnis) in enumerate(straipsniai):

#         url = 'https://www.15min.lt' + straipsnis

#         text = ''
#         res= urlopen('https://www.15min.lt' + straipsnis)
#         soup1 = BeautifulSoup(res.read(), 'html.parser')
        
#         title = soup1.find("h1", itemprop="headline").text.strip()
#         m = re.search(r"\w([^\"]*)(\.|!|\?)", str(soup1.select(".intro")))
#         try:
#           summary = m.group(0)
#         except:
#           summary = 'NERA'
            
#         for elm in soup1.select(".text p"):

            
#             if (len(text) > 3000):
#                 break
#             text += elm.text
#         text = text[0:3000]
            

#         print(a, end =" ")
#         df = df.append({'text' : text , 'author' : autorNames[offset + i], 'summary' : summary, 'title' : title }, ignore_index=True)

#     df.to_csv('/content/drive/MyDrive/vgtu/BAKALAURAS/temos-%i.csv' % (offset + i), sep='\t')
#     df = pandas.DataFrame(columns = col_names)
#     print('finish')
#     print('with current author')
