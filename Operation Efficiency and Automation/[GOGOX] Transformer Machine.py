#!/usr/bin/env python
# coding: utf-8

# In[12]:


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


# In[13]:


Admin_User_Email = str('xxxxxx')
Admin_User_Password = str('xxxx')

import glob
import os 
list_of_files = glob.glob('*.csv')
latest_file = max(list_of_files, key = os.path.getctime)
df = pd.read_csv(latest_file,index_col = False)

driver_link = {}
for i in range(0,len(df)):
    driver_link[i] = 'xxxxxxxxxxx'+ str(df['driver_id'][i]) 
driver_link_df = pd.DataFrame.from_dict(driver_link, orient='index', columns = ['driver_link'])
driver_link_batch_0 = driver_link_df
df


# In[14]:


browser_0 = webdriver.Chrome(executable_path='xxxxxx')
browser_0.get('xxxxxxxxx')
browser_0.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_0.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_0.find_element_by_id("admin_user_submit_action").click()

for i in range(0,len(driver_link_batch_0)):
    browser_0.get(driver_link_batch_0['driver_link'][i])
    time.sleep(2) 
    browser_0.find_element_by_xpath('//*[@id="active_admin_comment_body"]').send_keys(str(df['tag_name'][i]))
    browser_0.find_element_by_xpath('//*[@id="active_admin_comment_submit_action"]/input').click()
    time.sleep(2) 

browser_0.close()


# In[ ]:




