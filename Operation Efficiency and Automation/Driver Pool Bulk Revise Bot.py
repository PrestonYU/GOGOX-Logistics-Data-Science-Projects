#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium .webdriver.support.ui import Select 
import requests
from selenium.webdriver.common.keys import Keys
import pandas as pd 
import numpy as np 
from datetime import timedelta
import datetime


# In[4]:


df = pd.read_csv('xxxxx.csv')
df['pool_link'] = '-'
for i in range(0,len(df)):
    df['pool_link'][i] = 'xxxxxx' + str(df['Id'][i]) +'/pools'
dff = df[df['Pools'].str.contains('monthly_payments') == False]
dff = dff.reset_index(drop = True)
dff.head(50)


# In[ ]:





# In[ ]:





# In[5]:


Admin_User_Email = str('xxxxxxx')
Admin_User_Password = str('xxxxxx')

SCROLL_PAUSE_TIME = 1
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument('--headless') # 啟動無頭模式

browser = webdriver.Chrome(executable_path='xxxxx',options=chrome_options)
browser.get('xxxxxxx')
browser.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

browser1 = webdriver.Chrome(executable_path='xxxxxxx',options=chrome_options)
browser1.get('xxxxxx')
browser1.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser1.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser1.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

browser2 = webdriver.Chrome(executable_path='xxxxx',options=chrome_options)
browser2.get('xxxxxx')
browser2.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser2.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser2.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

browser3 = webdriver.Chrome(executable_path='xxxxxx',options=chrome_options)
browser3.get('xxxxxxx')
browser3.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser3.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser3.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

browser4 = webdriver.Chrome(executable_path='xxxxx',options=chrome_options)
browser4.get('xxxxxxxx')
browser4.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser4.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser4.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

for i in range(0,9000): 
    browser.get(dff['pool_link'][i])
    browser1.get(dff['pool_link'][9000+i])
    browser2.get(dff['pool_link'][18000+i])
    browser3.get(dff['pool_link'][27000+i])
    
    
    browser.find_element_by_xpath('//*[@id="driver_driver_pool_ids_1"]').click()
    browser.find_element_by_xpath('//*[@id="main_content"]/div/form/fieldset/input[34]').click()
    
    browser1.find_element_by_xpath('//*[@id="driver_driver_pool_ids_1"]').click()
    browser1.find_element_by_xpath('//*[@id="main_content"]/div/form/fieldset/input[34]').click()
    
    browser2.find_element_by_xpath('//*[@id="driver_driver_pool_ids_1"]').click()
    browser2.find_element_by_xpath('//*[@id="main_content"]/div/form/fieldset/input[34]').click()
    
    browser3.find_element_by_xpath('//*[@id="driver_driver_pool_ids_1"]').click()
    browser3.find_element_by_xpath('//*[@id="main_content"]/div/form/fieldset/input[34]').click()
    
    try:
        browser4.get(dff['pool_link'][36000+i])
        browser4.find_element_by_xpath('//*[@id="driver_driver_pool_ids_1"]').click()
        browser4.find_element_by_xpath('//*[@id="main_content"]/div/form/fieldset/input[34]').click()
    except:
        pass
    
    
    time.sleep(1)
    
    


# In[ ]:




