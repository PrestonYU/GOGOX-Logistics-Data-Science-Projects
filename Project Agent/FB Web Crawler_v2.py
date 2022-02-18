#!/usr/bin/env python
# coding: utf-8

# In[557]:


import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from selenium.webdriver import ActionChains
import re

# Login 
# you have to download "chromedriver" and put it in specific file path
browser = webdriver.Chrome(executable_path='/Applications/Google Chrome.app/Contents/MacOS/chromedriver')
browser.get('https://www.facebook.com')

browser.find_element_by_id("email").send_keys('xxxxxxxx') # USERNAME - you have to change the * part to your email address
browser.find_element_by_id("pass").send_keys('xxxxxxxxx')     # PASSWORD - you have to change the * part to your password
browser.find_element_by_id("u_0_b").click()
time.sleep(5)
browser.find_element_by_xpath('//*[@id="facebook"]/body').click()   # Counter anti-crawler mechanism

post_link = {}
post_creater_name = {}
post_creater_profile = {}
post_message = {}

replier_log = {}
replier_name = {}
replier_profile = {}
replier_destination = {}

####################
## Start Crawling ##
####################

browser.get('https://www.facebook.com/groups/xxxxxxx')
SCROLL_PAUSE_TIME = 2
time.sleep(5)
try:
    browser.find_element_by_xpath('//*[@id="facebook"]').click()   # Counter anti-crawler mechanism
except:
    time.sleep(1)

# Selenium Scroll Down Action Simulation - Iteration 20 times
last_height = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
i = 0 
while i <= 3:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #print('網頁更新中...')
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = browser.execute_script("return document.body.scrollHeight")
    i = i+1
    if new_height == last_height:
    #print('到達頁面底端')
        break
            
    last_height = new_height

# 爬取網頁內容，解析後萃取摘要
html = browser.page_source
soup = BeautifulSoup(html, "lxml") 

group_block = soup.find_all(href=re.compile("./permalink/."))
for i in range(0,len(group_block)):
    post_link[i] = group_block[i].get('href') #post_link

    
######################
## Post Detail Page ##
######################

for j in range(0,len(post_link)):
    if '/groups/471895053425494' in post_link[j]:
        try:
            browser.get(post_link[j])
            time.sleep(3)
            #browser.find_element_by_xpath('//*[@id="facebook"]').click()   # Counter anti-crawler mechanism

            last_height = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i = 0 
            while i<=5:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #print('網頁更新中...')
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = browser.execute_script("return document.body.scrollHeight")
                i = i+1
                if new_height == last_height:
                    #print('到達頁面底端')
                    break
            
                last_height = new_height
                time.sleep(3)

            html = browser.page_source
            soup = BeautifulSoup(html, "lxml") 

            group_block = soup.find_all('div',attrs={'data-ad-comet-preview':'message'})
            try:
                post_message[j] = group_block[0].get_text() #post_message
            except:
                post_message[j] = ''

            group_block = soup.find_all(href=re.compile("./user/."),attrs={'role':'link'})
            '''
            group_block.remove(group_block[19])
            group_block.remove(group_block[18])
            group_block.remove(group_block[17])
            group_block.remove(group_block[16])
            group_block.remove(group_block[15])
            group_block.remove(group_block[14])
            group_block.remove(group_block[13])
            group_block.remove(group_block[12])
            group_block.remove(group_block[11])
            group_block.remove(group_block[10])
            group_block.remove(group_block[9])
            group_block.remove(group_block[8])
            group_block.remove(group_block[7])
            group_block.remove(group_block[6])
            group_block.remove(group_block[5])
            group_block.remove(group_block[4])
            group_block.remove(group_block[3])
            group_block.remove(group_block[2])
            group_block.remove(group_block[1])
            group_block.remove(group_block[0])
            '''
            try:
                post_creater_profile[j] = 'https://facebook.com'+str(group_block[0].get('href')) #post_creater_profile
                post_creater_name[j] = group_block[0].get('aria-label') #post_creater_name
            except:
                post_creater_profile[j] = ''
                post_creater_name[j] = ''

            
            group_block = soup.find_all(attrs={'class':'_680y'})
            for k in range(0,len(group_block)):
                try:
                    replier_log[len(replier_name)] = j
                    replier_destination[len(replier_name)] = post_link[j] #for loop -> replier_destination
                    replier_name[len(replier_name)] = group_block[k].find_all('span')[0].get_text() #for loop -> replier_name
                    replier_profile[len(replier_profile)] = group_block[k].find_all('span')[0].find_all('a')[0].get('href') #for loop -> replier_profile
                except:
                    continue
                    
        except:
            post_message[j] = ''
            post_creater_profile[j] = ''
            post_creater_name[j] = ''
            replier_name[len(replier_name)] = ''
            replier_profile[len(replier_profile)] = ''
            replier_destination[len(replier_destination)] = ''
            
    else:
        post_message[j] = ''
        post_creater_profile[j] = ''
        post_creater_name[j] = ''
        replier_name[len(replier_name)] = ''
        replier_profile[len(replier_profile)] = ''
        replier_destination[len(replier_destination)] = ''

        
        
###############
## DataFrame ##
###############        
        

post_message_df = pd.DataFrame.from_dict(post_message,orient='index')
post_message_df = post_message_df.reset_index(drop=True)
post_creater_profile_df = pd.DataFrame.from_dict(post_creater_profile,orient='index')
post_creater_profile_df = post_creater_profile_df.reset_index(drop=True)
post_creater_name_df = pd.DataFrame.from_dict(post_creater_name,orient='index')
post_creater_name_df = post_creater_name_df.reset_index(drop=True)

post_link_df = pd.DataFrame.from_dict(post_link,orient='index')
post_link_df = post_link_df.reset_index(drop=True)

replier_name_df = pd.DataFrame.from_dict(replier_name,orient='index')
replier_name_df = replier_name_df.reset_index(drop=True)
replier_profile_df = pd.DataFrame.from_dict(replier_profile,orient='index')
replier_profile_df = replier_profile_df.reset_index(drop=True)
replier_log_df = pd.DataFrame.from_dict(replier_log,orient='index')
replier_log_df = replier_log_df.reset_index(drop=True)
replier_destination_df = pd.DataFrame.from_dict(replier_destination,orient='index')
replier_destination_df = replier_destination_df.reset_index(drop=True)

    
post_df_list = [post_creater_name_df,post_message_df,post_link_df,post_creater_profile_df]
post_reply_df_list = [replier_name_df,replier_profile_df,replier_destination_df]

post_df = pd.concat(post_df_list , axis = 1)
post_df = post_df.reset_index(drop=True)

post_reply_df = pd.concat(post_reply_df_list , axis = 1)
post_reply_df = post_reply_df.reset_index(drop=True)

post_df.columns=['發文者','發文內容','文章連結','發文者詳細資料']
post_reply_df.columns=['留言者','留言者詳細資料','文章連結']

post_df = post_df[post_df['發文者'] != '']
post_df = post_df.drop_duplicates(subset=['發文內容'])
post_df = post_df.reset_index(drop=True)

post_reply_df = post_reply_df[post_reply_df['留言者'] != '']
post_reply_df = post_reply_df[post_reply_df['留言者'] != 1]
post_reply_df = post_reply_df[post_reply_df['留言者詳細資料'].notnull()]
post_reply_df = post_reply_df.reset_index(drop=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# In[ ]:




