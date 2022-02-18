#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Import Google Sheet to Jupyter Notebook
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import numpy as np

# The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# Name of our Service Account Key
# https://console.developers.xxxxxxxxxx
google_key_file = 'xxxxxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

# Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('xxxxxxx')

# Selecting which sheet to pulling the data
sheet = workbook.worksheet('Payment Link Generation')

# Pulling the data and transform it to the data frame
values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[0])
df = df[1:]
df = df.reset_index(drop = True)


# In[11]:


df


# In[12]:


# Import selenium chromedriver
# Download Chromedriver : https://chromedriver.chromium.org/

import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select 
import requests
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np 

browser = webdriver.Chrome(executable_path='xxxxxxxx')
browser.get('https://portal.tappaysdk.com/xxxxxx')
# Insert Company Account No.: xxxx
# Insert User Email
# Insert User Password:xxxxxxxx
# Run reCAPTHCA
# Insert Verification Code
# Go on the following steps


# In[13]:


# Create Payment Order
for i in range(0,len(df)):
    browser.get('https://portal.tappaysdk.com/xxxxxxx')
    time.sleep(5)
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div/div[1]/button").click()

    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[2]/input").clear()
    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[2]/input").send_keys(df['訂單編號'][i])

    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[3]/input").clear()
    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[3]/input").send_keys(df['品項名稱'][i])

    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[4]/div[1]/div/input").clear()
    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[4]/div[1]/div/input").send_keys(df['費用'][i])

    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[4]/div[2]/input[1]").send_keys(Keys.BACKSPACE)
    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[4]/div[2]/input[1]").send_keys('3')

    checkboxs = browser.find_elements_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[6]/div[1]/div")
    for checkbox in checkboxs:
        checkbox.click()
    
    checkboxs = browser.find_elements_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[6]/div[2]/div")
    for checkbox in checkboxs:
        checkbox.click()
    
    checkboxs = browser.find_elements_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[7]/div[1]/div")
    for checkbox in checkboxs:
        checkbox.click()

    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[5]/input").clear()
    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[3]/div/form/div[5]/input").send_keys('有任何問題請聯繫LINE小幫手 xxxxxxx')
    browser.find_element_by_xpath("/html/body/div[3]/div[10]/div[4]/button").click()
    time.sleep(7)
    browser.find_element_by_xpath("/html/body/div[3]/div[2]/div[4]/div/button[2]").click() 


# In[14]:


# Set Filter 1: Creator email
# Set Filter 2: Status = 等待付款
# Set Sorting: Create time ascending order

SCROLL_PAUSE_TIME = 1

# Use Selenium to simulate the scroll down actions
last_height = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
while True:
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Purify the webpage results   
html = browser.page_source
soup = BeautifulSoup(html,"lxml")
group_block = soup.find('table',attrs={'class':'ui table selectable unstackable center aligned'})
group_block2 = group_block.find_all('tr')

l = []
for tr in group_block2:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    l.append(row)
linkdf = pd.DataFrame(l, columns = ['訂單編號','品項名稱','金額','日期','建立者','狀態','URL'])
linkdf


import clipboard
for j in range(0,len(linkdf)):
    # Copy Payment link
    browser.find_element_by_xpath('//*[@id="orders"]/tbody/tr['+ str(j+1) +']').click()
    browser.find_element_by_xpath('/html/body/div[3]/div[9]/div[3]/div/table[1]/tbody/tr[2]/td[2]/div/button').click()
    time.sleep(5)
    linkdf['URL'][j] = clipboard.paste()
    browser.find_element_by_xpath('/html/body/div[3]/div[9]/div[1]/button').click()


# In[15]:


# Backend Setting : https://console.developers.xxxxxxx
# Connect to Google Sheet
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
    
# Configure the connection
scope = ['https://spreadsheets.google.com/feeds']
    
# Give the path to the Service Account Credential 
credentials = ServiceAccountCredentials.from_json_keyfile_name('xxxxxxx')
    
# Authorize Jupyter Notebook
gc = gspread.authorize(credentials)
    
# The gsheet ID
# Sheet URL : https://docs.google.com/spreadsheets/d/xxxxxxx
spreadsheet_key = 'xxxxxxxx'
        
# Set the sheet name for uploading the dataframe
wks_name = 'Link_DF'
cell_of_start_df = 'A1'
    
    # Upload the dataframe
d2g.upload(linkdf,
            spreadsheet_key,
            wks_name,
            credentials = credentials,
            start_cell = cell_of_start_df,
            clean = True)


# In[ ]:




