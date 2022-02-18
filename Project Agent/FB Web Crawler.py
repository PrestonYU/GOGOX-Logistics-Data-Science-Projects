#!/usr/bin/env python
# coding: utf-8

# ## 1) Web Crawler Login

# In[1]:


import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np


# In[23]:


# Login 
browser = webdriver.Chrome(executable_path='xxxxxxx') # you have to download "chromedriver" and put it in specific file path
browser.get('https://www.facebook.com')
time.sleep(3)
browser.find_element_by_id("email").send_keys('*******') # USERNAME - you have to change the * part to your email address
browser.find_element_by_id("pass").send_keys('******')       # PASSWORD - you have to change the * part to your password
browser.find_element_by_id("u_0_b").click()


# ## 2) Bulk Web Crawling

# In[24]:


# Keyword List for querying - you can change to any keyword you would like to search in Facebook

s = {0:'購',
     1:'買',
     2:'團購',
     3:'代購',
     4:'代買',
     5:'二手',
     6:'市集',
     7:'購物',
     8:'代運',
     9:'商城',
     10:'批發',
     11:'零售',
     12:'舖',
     13:'小店',
     14:'雜貨',
     15:'特賣',
     16:'限量',
     17:'百貨',
     18:'販售',
     19:'販',
     20:'連線',
     21:'販賣',
     22:'拍賣'
    }

# Transfer to UTF-8 encoding

s_transfer_encode = {}

for i in range(0,len(s)):
    s_transfer_encode[i] = repr(s[i].encode('UTF-8')).upper().replace('\\X','%')[2:-1:1]


# In[25]:


# Create querying URL

fb_groups_url = {}
fb_pages_url = {}

for i in range(0,len(s_transfer_encode)):
    fb_groups_url[i] = 'https://www.facebook.com/search/groups/?q=' + str(s_transfer_encode[i])
    fb_pages_url[i] = 'https://www.facebook.com/search/pages?q=' + str(s_transfer_encode[i])


# In[26]:


fb_url = {}

for i in range(0,len(fb_groups_url)):
    fb_url[i] = fb_groups_url[i]
    
for j in range(0,len(fb_pages_url)):
    fb_url[len(fb_url)] = fb_pages_url[j]
    
fb_url


# In[27]:


fb_url_result = {}

for k in range(0,len(fb_url)):
    browser.get(fb_url[k])  # 打開瀏覽器並連到網頁
    SCROLL_PAUSE_TIME = 1
    
    # 以下是用Selenium模擬下拉網頁動作，讓網頁更新
    last_height = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
        #    print('到達頁面底端')
            break
        last_height = new_height

    
    # 爬取網頁內容，解析後萃取摘要
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")

    group_block = soup.find_all('div', attrs={'class':'nc684nl6'})
    group_block2 = soup.find_all('span', attrs={'class':'oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql a8c37x1j muag1w35 dco85op0 e9vueds3 j5wam9gi knj5qynh m9osqain'})

    group_name = {}
    group_link = {}
    group_member = {}

    for i, group_item in enumerate(group_block):    
        #print("----------------------------------------------------------------------")
        group_body = group_item.find('span')
        group_url = group_item.find('a')["href"]
        #print(str(group_body).strip('<span>').strip('</'))
        group_name[i] = str(group_body).strip('<span>').strip('</')
        
        externalLink = group_url + 'about'
        #print(externalLink)
        group_link[i] = str(externalLink)
        
        j == i
        
        for j, group_item2 in enumerate(group_block2):
            if j == i:
                group_mem = group_item2.find('span', attrs = {'class':'oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql e9vueds3 j5wam9gi knj5qynh m9osqain a8c37x1j ni8dbmo4 stjgntxs ltmttdrg g0qnabr5'})
                #print(str(group_mem).strip('<span class="oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql e9vueds3 j5wam9gi knj5qynh m9osqain a8c37x1j ni8dbmo4 stjgntxs ltmttdrg g0qnabr5" dir="auto">').strip('</'))
                group_member[i] = str(group_mem).strip('<span class="oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql e9vueds3 j5wam9gi knj5qynh m9osqain a8c37x1j ni8dbmo4 stjgntxs ltmttdrg g0qnabr5" dir="auto">').strip('</')
            else:
                pass 
    
    # 繪製表格
    fb_group_name_df = pd.DataFrame.from_dict(group_name, orient='index',columns=['group_name'])
    fb_group_link_df = pd.DataFrame.from_dict(group_link, orient='index',columns=['group_link'])
    fb_group_df = pd.concat([fb_group_name_df,fb_group_link_df],axis = 1)
    fb_group_member_df = pd.DataFrame.from_dict(group_member, orient='index',columns=['group_member'])
    fb_group_df = pd.concat([fb_group_df,fb_group_member_df],axis = 1)
    fb_url_result[k] = fb_group_df


# In[28]:


fb_url_result_df = fb_url_result[0]

for i in range(1,len(fb_url_result)):
    fb_url_result_df = pd.concat([fb_url_result_df,fb_url_result[i]],axis = 0)
    
fb_url_result_df


# In[8]:


fb_url_result_df.to_csv('fb_url_result_df.csv',index=False)


# ## 3) Match with EC

# In[9]:


fb_url_result_df = fb_url_result_df.reset_index(drop=True)


# In[10]:


import re 

# 群組全名 - 英文部分
fb_url_result_df['group_name_en'] = fb_url_result_df['group_name']

for i in range(0,len(fb_url_result_df)):
    text = fb_url_result_df['group_name_en'][i]
    fb_url_result_df['group_name_en'][i] = re.sub('[^0-9A-Za-z]', '', text) 


# In[11]:


# 群組全名 - 中文部分
fb_url_result_df['group_name_ch'] = fb_url_result_df['group_name']

for i in range(0,len(fb_url_result_df)):
    text = fb_url_result_df['group_name_ch'][i]
    fb_url_result_df['group_name_ch'][i] = re.sub('[^0-9\u4e00-\u9fa5]', '', text) 


# In[12]:


# 群組全名 - 中文部分 - 2 gram
fb_url_result_df['group_name_ch_2g'] = fb_url_result_df['group_name_ch']

for i in range(0,len(fb_url_result_df)):
    fb_url_result_df['group_name_ch_2g'][i] = fb_url_result_df['group_name_ch'][i][:2]


# In[13]:


# 群組全名 - 中文部分 - 3 gram
fb_url_result_df['group_name_ch_3g'] = fb_url_result_df['group_name_ch']

for i in range(0,len(fb_url_result_df)):
    fb_url_result_df['group_name_ch_3g'][i] = fb_url_result_df['group_name_ch'][i][:3]


# In[14]:


# 群組全名 - 中文部分 - 4 gram
fb_url_result_df['group_name_ch_4g'] = fb_url_result_df['group_name_ch']

for i in range(0,len(fb_url_result_df)):
    fb_url_result_df['group_name_ch_4g'][i] = fb_url_result_df['group_name_ch'][i][:4]


# In[15]:


# 群組全名 - 中文部分 - 5 gram
fb_url_result_df['group_name_ch_5g'] = fb_url_result_df['group_name_ch']

for i in range(0,len(fb_url_result_df)):
    fb_url_result_df['group_name_ch_5g'][i] = fb_url_result_df['group_name_ch'][i][:5]


# In[16]:


# 群組全名 - 中文部分 - 6 gram
fb_url_result_df['group_name_ch_6g'] = fb_url_result_df['group_name_ch']

for i in range(0,len(fb_url_result_df)):
    fb_url_result_df['group_name_ch_6g'][i] = fb_url_result_df['group_name_ch'][i][:6]


# In[17]:


shopee_url_ch = {}
shopee_url_en = {}
shopee_url_ch_2g = {}
shopee_url_ch_3g = {}
shopee_url_ch_4g = {}
shopee_url_ch_5g = {}
shopee_url_ch_6g = {}

for i in range(0,len(fb_url_result_df)):
    shopee_url_ch[i] = 'https://shopee.tw/search?keyword=' + str(fb_url_result_df['group_name_ch'][i])

for i in range(0,len(fb_url_result_df)):
    shopee_url_en[i] = 'https://shopee.tw/search?keyword=' + str(fb_url_result_df['group_name_en'][i])

for i in range(0,len(fb_url_result_df)):
    shopee_url_ch_2g[i] = 'https://shopee.tw/search?keyword=' + str(fb_url_result_df['group_name_ch_2g'][i])

for i in range(0,len(fb_url_result_df)):
    shopee_url_ch_3g[i] = 'https://shopee.tw/search?keyword=' + str(fb_url_result_df['group_name_ch_3g'][i])

for i in range(0,len(fb_url_result_df)):
    shopee_url_ch_4g[i] = 'https://shopee.tw/search?keyword=' + str(fb_url_result_df['group_name_ch_4g'][i])

for i in range(0,len(fb_url_result_df)):
    shopee_url_ch_5g[i] = 'https://shopee.tw/search?keyword=' + str(fb_url_result_df['group_name_ch_5g'][i])
    
for i in range(0,len(fb_url_result_df)):
    shopee_url_ch_6g[i] = 'https://shopee.tw/search?keyword=' + str(fb_url_result_df['group_name_ch_6g'][i])


# In[18]:


# Parallel Crawling - it might take time (need at least 1 hours) to crawl these websites

browser_0 = webdriver.Chrome(executable_path='xxxxxxx')
browser_1 = webdriver.Chrome(executable_path='xxxxxxx')
browser_2 = webdriver.Chrome(executable_path='xxxxxxx')
browser_3 = webdriver.Chrome(executable_path='xxxxxxx')
browser_4 = webdriver.Chrome(executable_path='xxxxxxx')
browser_5 = webdriver.Chrome(executable_path='xxxxxxx')
browser_6 = webdriver.Chrome(executable_path='xxxxxxx')

sp_nickname_0 = {}
sp_nickname_1 = {}
sp_nickname_2 = {}
sp_nickname_3 = {}
sp_nickname_4 = {}
sp_nickname_5 = {}
sp_nickname_6 = {}
    
sp_username_0 = {}
sp_username_1 = {}
sp_username_2 = {}
sp_username_3 = {}
sp_username_4 = {}
sp_username_5 = {}
sp_username_6 = {}
    
sp_follower_0 = {}
sp_follower_1 = {}
sp_follower_2 = {}
sp_follower_3 = {}
sp_follower_4 = {}
sp_follower_5 = {}
sp_follower_6 = {}


for i in range(0,len(shopee_url_ch)):
    
    # 打開瀏覽器並連到網頁
    browser_0.get(shopee_url_ch[i])  
    browser_1.get(shopee_url_en[i])  
    browser_2.get(shopee_url_ch_2g[i]) 
    browser_3.get(shopee_url_ch_3g[i]) 
    browser_4.get(shopee_url_ch_4g[i])  
    browser_5.get(shopee_url_ch_5g[i])  
    browser_6.get(shopee_url_ch_6g[i])  
    
    SCROLL_PAUSE_TIME = 0.5
    
    # 用Selenium模擬下拉網頁動作，讓網頁更新
    last_height_0 = browser_0.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser_0.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height_0 = browser_0.execute_script("return document.body.scrollHeight")
        if new_height_0 == last_height_0:
            #print('到達頁面底端')
            break
            
        last_height_0 = new_height_0
    
    
    last_height_1 = browser_1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser_1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height_1 = browser_1.execute_script("return document.body.scrollHeight")
        if new_height_1 == last_height_1:
            #print('到達頁面底端')
            break
            
        last_height_1 = new_height_1
        
        
    last_height_2 = browser_2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser_2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height_2 = browser_2.execute_script("return document.body.scrollHeight")
        if new_height_2 == last_height_2:
            #print('到達頁面底端')
            break
            
        last_height_2 = new_height_2
    
    
    last_height_3 = browser_3.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser_3.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height_3 = browser_3.execute_script("return document.body.scrollHeight")
        if new_height_3 == last_height_3:
            #print('到達頁面底端')
            break
            
        last_height_3 = new_height_3
    
    
    last_height_4 = browser_4.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser_4.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height_4 = browser_4.execute_script("return document.body.scrollHeight")
        if new_height_4 == last_height_4:
            #print('到達頁面底端')
            break
            
        last_height_4 = new_height_4
    
    
    last_height_5 = browser_5.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser_5.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height_5 = browser_5.execute_script("return document.body.scrollHeight")
        if new_height_5 == last_height_5:
            #print('到達頁面底端')
            break
            
        last_height_5 = new_height_5
        
        
    last_height_6 = browser_6.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    while True:
        browser_6.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #print('網頁更新中...')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height_6 = browser_6.execute_script("return document.body.scrollHeight")
        if new_height_6 == last_height_6:
            #print('到達頁面底端')
            break
            
        last_height_6 = new_height_6
        

    # 爬取網頁內容，解析後萃取摘要
    html_0 = browser_0.page_source
    soup_0 = BeautifulSoup(html_0, "lxml")  
    html_1 = browser_1.page_source
    soup_1 = BeautifulSoup(html_1, "lxml") 
    html_2 = browser_2.page_source
    soup_2 = BeautifulSoup(html_2, "lxml") 
    html_3 = browser_3.page_source
    soup_3 = BeautifulSoup(html_3, "lxml") 
    html_4 = browser_4.page_source
    soup_4 = BeautifulSoup(html_4, "lxml") 
    html_5 = browser_5.page_source
    soup_5 = BeautifulSoup(html_5, "lxml") 
    html_6 = browser_6.page_source
    soup_6 = BeautifulSoup(html_6, "lxml") 
    
    
    #0
    try:
        group_block_0 = soup_0.find_all('div', attrs={'class':'shopee-search-user-item__nickname'})
        sp_nickname_0[i] = str(group_block_0[0]).strip('<div class="shopee-search-user-item__nickname">').strip('</')
    except:
        sp_nickname_0[i] = 'Null'
    
    try:
        group_block2_0 = soup_0.find_all('div', attrs={'class':'shopee-search-user-item__username'})
        sp_username_0[i] = str(group_block2_0[0]).strip('<div class="shopee-search-user-item__username').strip('>').strip('</div')
    except:
        sp_username_0[i] = 'Null'
    
    try:
        group_block3_0 = soup_0.find_all('span', attrs={'class':'shopee-search-user-item__follow-count-number'})
        sp_follower_0[i] = str(group_block3_0[0]).strip('"<span class="shopee-search-user-item__follow-count-number"').strip('>').strip('</span') + '粉絲'
    except:
        sp_follower_0[i] = 'Null'
    
    #1
    try:
        group_block_1 = soup_1.find_all('div', attrs={'class':'shopee-search-user-item__nickname'})
        sp_nickname_1[i] = str(group_block_1[0]).strip('<div class="shopee-search-user-item__nickname">').strip('</')
    except:
        sp_nickname_1[i] = 'Null'
    
    try:
        group_block2_1 = soup_1.find_all('div', attrs={'class':'shopee-search-user-item__username'})
        sp_username_1[i] = str(group_block2_1[0]).strip('<div class="shopee-search-user-item__username').strip('>').strip('</div')
    except:
        sp_username_1[i] = 'Null'
    
    try:
        group_block3_1 = soup_1.find_all('span', attrs={'class':'shopee-search-user-item__follow-count-number'})
        sp_follower_1[i] = str(group_block3_1[0]).strip('"<span class="shopee-search-user-item__follow-count-number"').strip('>').strip('</span') + '粉絲'
    except:
        sp_follower_1[i] = 'Null'
        
    #2
    try:
        group_block_2 = soup_2.find_all('div', attrs={'class':'shopee-search-user-item__nickname'})
        sp_nickname_2[i] = str(group_block_2[0]).strip('<div class="shopee-search-user-item__nickname">').strip('</')
    except:
        sp_nickname_2[i] = 'Null'
    
    try:
        group_block2_2 = soup_2.find_all('div', attrs={'class':'shopee-search-user-item__username'})
        sp_username_2[i] = str(group_block2_2[0]).strip('<div class="shopee-search-user-item__username').strip('>').strip('</div')
    except:
        sp_username_2[i] = 'Null'
    
    try:
        group_block3_2 = soup_2.find_all('span', attrs={'class':'shopee-search-user-item__follow-count-number'})
        sp_follower_2[i] = str(group_block3_2[0]).strip('"<span class="shopee-search-user-item__follow-count-number"').strip('>').strip('</span') + '粉絲'
    except:
        sp_follower_2[i] = 'Null'
        
    #3
    try:
        group_block_3 = soup_3.find_all('div', attrs={'class':'shopee-search-user-item__nickname'})
        sp_nickname_3[i] = str(group_block_3[0]).strip('<div class="shopee-search-user-item__nickname">').strip('</')
    except:
        sp_nickname_3[i] = 'Null'
    
    try:
        group_block2_3 = soup_3.find_all('div', attrs={'class':'shopee-search-user-item__username'})
        sp_username_3[i] = str(group_block2_3[0]).strip('<div class="shopee-search-user-item__username').strip('>').strip('</div')
    except:
        sp_username_3[i] = 'Null'
    
    try:
        group_block3_3 = soup_3.find_all('span', attrs={'class':'shopee-search-user-item__follow-count-number'})
        sp_follower_3[i] = str(group_block3_3[0]).strip('"<span class="shopee-search-user-item__follow-count-number"').strip('>').strip('</span') + '粉絲'
    except:
        sp_follower_3[i] = 'Null'

    #4
    try:
        group_block_4 = soup_4.find_all('div', attrs={'class':'shopee-search-user-item__nickname'})
        sp_nickname_4[i] = str(group_block_4[0]).strip('<div class="shopee-search-user-item__nickname">').strip('</')
    except:
        sp_nickname_4[i] = 'Null'
    
    try:
        group_block2_4 = soup_4.find_all('div', attrs={'class':'shopee-search-user-item__username'})
        sp_username_4[i] = str(group_block2_4[0]).strip('<div class="shopee-search-user-item__username').strip('>').strip('</div')
    except:
        sp_username_4[i] = 'Null'
    
    try:
        group_block3_4 = soup_4.find_all('span', attrs={'class':'shopee-search-user-item__follow-count-number'})
        sp_follower_4[i] = str(group_block3_4[0]).strip('"<span class="shopee-search-user-item__follow-count-number"').strip('>').strip('</span') + '粉絲'
    except:
        sp_follower_4[i] = 'Null'
    
    #5
    try:
        group_block_5 = soup_5.find_all('div', attrs={'class':'shopee-search-user-item__nickname'})
        sp_nickname_5[i] = str(group_block_5[0]).strip('<div class="shopee-search-user-item__nickname">').strip('</')
    except:
        sp_nickname_5[i] = 'Null'
    
    try:
        group_block2_5 = soup_5.find_all('div', attrs={'class':'shopee-search-user-item__username'})
        sp_username_5[i] = str(group_block2_5[0]).strip('<div class="shopee-search-user-item__username').strip('>').strip('</div')
    except:
        sp_username_5[i] = 'Null'
    
    try:
        group_block3_5 = soup_5.find_all('span', attrs={'class':'shopee-search-user-item__follow-count-number'})
        sp_follower_5[i] = str(group_block3_5[0]).strip('"<span class="shopee-search-user-item__follow-count-number"').strip('>').strip('</span') + '粉絲'
    except:
        sp_follower_5[i] = 'Null'
    
    #6
    try:
        group_block_6 = soup_6.find_all('div', attrs={'class':'shopee-search-user-item__nickname'})
        sp_nickname_6[i] = str(group_block_6[0]).strip('<div class="shopee-search-user-item__nickname">').strip('</')
    except:
        sp_nickname_6[i] = 'Null'
    
    try:
        group_block2_6 = soup_6.find_all('div', attrs={'class':'shopee-search-user-item__username'})
        sp_username_6[i] = str(group_block2_6[0]).strip('<div class="shopee-search-user-item__username').strip('>').strip('</div')
    except:
        sp_username_6[i] = 'Null'
    
    try:
        group_block3_6 = soup_6.find_all('span', attrs={'class':'shopee-search-user-item__follow-count-number'})
        sp_follower_6[i] = str(group_block3_6[0]).strip('"<span class="shopee-search-user-item__follow-count-number"').strip('>').strip('</span') + '粉絲'
    except:
        sp_follower_6[i] = 'Null'
    
    
# 繪製表格
sp_nickname_df_0 = pd.DataFrame.from_dict(sp_nickname_0, orient='index',columns=['nickname_0'])
sp_username_df_0 = pd.DataFrame.from_dict(sp_username_0, orient='index',columns=['username_0'])
sp_follower_df_0 = pd.DataFrame.from_dict(sp_follower_0, orient='index',columns=['follower_0'])
shopee_url_result_ch = pd.concat([sp_nickname_df_0,sp_username_df_0],axis = 1)
shopee_url_result_ch = pd.concat([shopee_url_result_ch,sp_follower_df_0],axis = 1)

sp_nickname_df_1 = pd.DataFrame.from_dict(sp_nickname_1, orient='index',columns=['nickname_1'])
sp_username_df_1 = pd.DataFrame.from_dict(sp_username_1, orient='index',columns=['username_1'])
sp_follower_df_1 = pd.DataFrame.from_dict(sp_follower_1, orient='index',columns=['follower_1'])
shopee_url_result_en = pd.concat([sp_nickname_df_1,sp_username_df_1],axis = 1)
shopee_url_result_en = pd.concat([shopee_url_result_en,sp_follower_df_1],axis = 1)

sp_nickname_df_2 = pd.DataFrame.from_dict(sp_nickname_2, orient='index',columns=['nickname_2'])
sp_username_df_2 = pd.DataFrame.from_dict(sp_username_2, orient='index',columns=['username_2'])
sp_follower_df_2 = pd.DataFrame.from_dict(sp_follower_2, orient='index',columns=['follower_2'])
shopee_url_result_ch_2g = pd.concat([sp_nickname_df_2,sp_username_df_2],axis = 1)
shopee_url_result_ch_2g = pd.concat([shopee_url_result_ch_2g,sp_follower_df_2],axis = 1)

sp_nickname_df_3 = pd.DataFrame.from_dict(sp_nickname_3, orient='index',columns=['nickname_3'])
sp_username_df_3 = pd.DataFrame.from_dict(sp_username_3, orient='index',columns=['username_3'])
sp_follower_df_3 = pd.DataFrame.from_dict(sp_follower_3, orient='index',columns=['follower_3'])
shopee_url_result_ch_3g = pd.concat([sp_nickname_df_3,sp_username_df_3],axis = 1)
shopee_url_result_ch_3g = pd.concat([shopee_url_result_ch_3g,sp_follower_df_3],axis = 1)

sp_nickname_df_4 = pd.DataFrame.from_dict(sp_nickname_4, orient='index',columns=['nickname_4'])
sp_username_df_4 = pd.DataFrame.from_dict(sp_username_4, orient='index',columns=['username_4'])
sp_follower_df_4 = pd.DataFrame.from_dict(sp_follower_4, orient='index',columns=['follower_4'])
shopee_url_result_ch_4g = pd.concat([sp_nickname_df_4,sp_username_df_4],axis = 1)
shopee_url_result_ch_4g = pd.concat([shopee_url_result_ch_4g,sp_follower_df_4],axis = 1)

sp_nickname_df_5 = pd.DataFrame.from_dict(sp_nickname_5, orient='index',columns=['nickname_5'])
sp_username_df_5 = pd.DataFrame.from_dict(sp_username_5, orient='index',columns=['username_5'])
sp_follower_df_5 = pd.DataFrame.from_dict(sp_follower_5, orient='index',columns=['follower_5'])
shopee_url_result_ch_5g = pd.concat([sp_nickname_df_5,sp_username_df_5],axis = 1)
shopee_url_result_ch_5g = pd.concat([shopee_url_result_ch_5g,sp_follower_df_5],axis = 1)

sp_nickname_df_6 = pd.DataFrame.from_dict(sp_nickname_6, orient='index',columns=['nickname_6'])
sp_username_df_6 = pd.DataFrame.from_dict(sp_username_6, orient='index',columns=['username_6'])
sp_follower_df_6 = pd.DataFrame.from_dict(sp_follower_6, orient='index',columns=['follower_6'])
shopee_url_result_ch_6g = pd.concat([sp_nickname_df_6,sp_username_df_6],axis = 1)
shopee_url_result_ch_6g = pd.concat([shopee_url_result_ch_6g,sp_follower_df_6],axis = 1)


# In[19]:


shopee_url_result_ch.to_csv("shopee_url_result_ch.csv")
shopee_url_result_en.to_csv("shopee_url_result_en.csv")
shopee_url_result_ch_2g.to_csv("shopee_url_result_ch_2g.csv")
shopee_url_result_ch_3g.to_csv("shopee_url_result_ch_3g.csv")
shopee_url_result_ch_4g.to_csv("shopee_url_result_ch_4g.csv")
shopee_url_result_ch_5g.to_csv("shopee_url_result_ch_5g.csv")
shopee_url_result_ch_6g.to_csv("shopee_url_result_ch_6g.csv")


# In[21]:


crawler_result_all_df = pd.concat([fb_url_result_df,shopee_url_result_ch,shopee_url_result_en,shopee_url_result_ch_2g,shopee_url_result_ch_3g,shopee_url_result_ch_4g,shopee_url_result_ch_5g,shopee_url_result_ch_6g],axis = 1)
crawler_result_all_df


# In[22]:


crawler_result_all_df.to_csv('crawler_result_all_df.csv')


# In[ ]:




