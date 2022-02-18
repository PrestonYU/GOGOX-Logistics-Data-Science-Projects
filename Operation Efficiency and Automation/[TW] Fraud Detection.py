#!/usr/bin/env python
# coding: utf-8

# In[18]:


# import selenium chromedriver
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select 
import requests
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np 
from datetime import timedelta
import datetime


# In[19]:


# Load Google Spreadsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
google_key_file = 'xxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

workbook = gc.open_by_key('xxxxxxx')
sheet = workbook.worksheet('Valicious Proxy Buying')

values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[0])
df = df[1:]
df = df.reset_index(drop = True)
df


# In[24]:


# Load Google Spreadsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
google_key_file = 'xxxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

workbook = gc.open_by_key('xxxxxxx')
sheet = workbook.worksheet('Valicious Proxy Buying')

values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[0])
df = df[1:]
df = df.reset_index(drop = True)


Admin_User_Email = str('xxxxxxxx')
Admin_User_Password = str('xxxxxxxx')
 
browser_0 = webdriver.Chrome(executable_path='xxxxxxx')
browser_1 = webdriver.Chrome(executable_path='xxxxxxxx')
browser_2 = webdriver.Chrome(executable_path='xxxxxxx')
browser_3 = webdriver.Chrome(executable_path='xxxxxx') 

browser_0.get('xxxxxx')
browser_1.get('xxxxxxx')
browser_2.get('xxxxxx')
browser_3.get('xxxxx')

browser_0.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_0.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_0.find_element_by_id("admin_user_submit_action").click()

browser_1.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_1.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_1.find_element_by_id("admin_user_submit_action").click()

browser_2.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_2.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_2.find_element_by_id("admin_user_submit_action").click()

browser_3.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_3.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_3.find_element_by_id("admin_user_submit_action").click()


while True:

    # Generate Fraud Client udid site link
    one_hour_before = (datetime.datetime.now() - timedelta(minutes = 15)).strftime("%Y-%m-%d+") + (datetime.datetime.now() - timedelta(minutes = 15)).strftime("%H")  + '%3A' + (datetime.datetime.now() - timedelta(minutes = 15)).strftime("%M")

    link = {} 

    # Generate Query Pages
    for i in range(0,len(df)):
        link[i] = 'xxxxxxx'+ one_hour_before + '&q%5Bclient_udid_equals%5D='+ str(df.loc[i][0]) +'&commit=Filter&order=id_desc'
        
    # Parallel Web Crawler
    for i in range(0,int(len(link)/4)):
        browser_0.get(link[i])
        browser_1.get(link[int(len(link)/4)+i])
        browser_2.get(link[int(len(link)*2/4)+i])
        browser_3.get(link[int(len(link)*3/4)+i])
    
        order_url_0 = {}
        order_url_1 = {}
        order_url_2 = {}
        order_url_3 = {}
    
        
        SCROLL_PAUSE_TIME = 1

        # Use Selenium to simulate the scroll down actions
        last_height_0 = browser_0.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        while True:
            browser_0.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height_0 = browser_0.execute_script("return document.body.scrollHeight")
            if new_height_0 == last_height_0:
                break
            last_height_0 = new_height_0
    
        last_height_1 = browser_1.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        while True:
            browser_1.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height_1 = browser_1.execute_script("return document.body.scrollHeight")
            if new_height_1 == last_height_1:
                break
            last_height_1 = new_height_1
        
        last_height_2 = browser_2.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        while True:
            browser_2.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height_2 = browser_2.execute_script("return document.body.scrollHeight")
            if new_height_2 == last_height_2:
                break
            last_height_2 = new_height_2  
        
        last_height_3 = browser_3.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        while True:
            browser_3.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height_3 = browser_3.execute_script("return document.body.scrollHeight")
            if new_height_3 == last_height_3:
                break
            last_height_3 = new_height_3  
          
        # Purify the webpage results   
        html_0 = browser_0.page_source
        soup_0 = BeautifulSoup(html_0,"lxml")
    
        html_1 = browser_1.page_source
        soup_1 = BeautifulSoup(html_1,"lxml")
    
        html_2 = browser_2.page_source
        soup_2 = BeautifulSoup(html_2,"lxml")
        
        html_3 = browser_3.page_source
        soup_3 = BeautifulSoup(html_3,"lxml")
    
        # browser_0
        try:
            group_block_0 = soup_0.find_all('td',attrs={'class':'col col-id'})
            for j, group_item_0 in enumerate(group_block_0):
                group_url_0 = group_item_0.find('a')["href"]
                order_url_0[j] = "xxxxxxx" + str(group_url_0) + "/edit"
            
            # order edit webpage --> select 'canceled' and upload notes 
            for k in range(0,len(order_url_0)):
                browser_0.get(order_url_0[k])
                s0 = Select(browser_0.find_element_by_id("order_request_status_cd"))
                s0.select_by_value("4")

                browser_0.find_element_by_id("order_request_notes").send_keys("疑似詐騙訂單")
                browser_0.find_element_by_id("order_request_submit_action").click()
        
        except: 
            continue
    
        # browser_1
        try:
            group_block_1 = soup_1.find_all('td',attrs={'class':'col col-id'})
            for j, group_item_1 in enumerate(group_block_1):
                group_url_1 = group_item_1.find('a')["href"]
                order_url_1[j] = "xxxxxxx" + str(group_url_1) + "/edit"
            
            # order edit webpage --> select 'canceled' and upload notes 
            for k in range(0,len(order_url_1)):
                browser_1.get(order_url_1[k])
                s1 = Select(browser_1.find_element_by_id("order_request_status_cd"))
                s1.select_by_value("4")

                browser_1.find_element_by_id("order_request_notes").send_keys("疑似詐騙訂單")
                browser_1.find_element_by_id("order_request_submit_action").click()
        
        except: 
            continue    

        # browser_2
        try:
            group_block_2 = soup_2.find_all('td',attrs={'class':'col col-id'})
            for j, group_item_2 in enumerate(group_block_2):
                group_url_2 = group_item_2.find('a')["href"]
                order_url_2[j] = "xxxxxxx" + str(group_url_2) + "/edit"
            
            # order edit webpage --> select 'canceled' and upload notes 
            for k in range(0,len(order_url_2)):
                browser_2.get(order_url_2[k])
                s2 = Select(browser_2.find_element_by_id("order_request_status_cd"))
                s2.select_by_value("4")

                browser_2.find_element_by_id("order_request_notes").send_keys("疑似詐騙訂單")
                browser_2.find_element_by_id("order_request_submit_action").click()
        
        except: 
            continue 
        
        # browser_3
        try:
            group_block_3 = soup_3.find_all('td',attrs={'class':'col col-id'})
            for j, group_item_3 in enumerate(group_block_3):
                group_url_3 = group_item_3.find('a')["href"]
                order_url_3[j] = "xxxxxx" + str(group_url_3) + "/edit"
            
            # order edit webpage --> select 'canceled' and upload notes 
            for k in range(0,len(order_url_3)):
                browser_3.get(order_url_3[k])
                s3 = Select(browser_3.find_element_by_id("order_request_status_cd"))
                s3.select_by_value("4")

                browser_3.find_element_by_id("order_request_notes").send_keys("疑似詐騙訂單")
                browser_3.find_element_by_id("order_request_submit_action").click()
        
        except: 
            continue 
    
    time.sleep(60)    
    


# In[ ]:




