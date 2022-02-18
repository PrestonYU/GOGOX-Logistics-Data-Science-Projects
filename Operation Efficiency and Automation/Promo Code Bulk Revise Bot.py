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


# In[15]:


Admin_User_Email = str('xxxxxxxx')
Admin_User_Password = str('xxxxxxxxx')

browser = webdriver.Chrome(executable_path='xxxxxxxxx')
browser.get('xxxxxxxxxxxxxx')
browser.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()
time.sleep(10)
browser.find_element_by_xpath('//*[@id="index_footer"]/div[2]/a[1]').click()
time.sleep(30)
browser.close()


import glob
import os 
list_of_files = glob.glob('*.csv')
latest_file = max(list_of_files, key = os.path.getctime)
df = pd.read_csv(latest_file,index_col = False)
df.head()


# In[19]:


Admin_User_Email = str('xxxxxxx')
Admin_User_Password = str('xxxxxx')

import glob
import os 
list_of_files = glob.glob('*.csv')
latest_file = max(list_of_files, key = os.path.getctime)
df = pd.read_csv(latest_file,index_col = False)

promo_link = {}
for i in range(0,len(df)):
    promo_link[i] = 'xxxxxxxx'+ str(df['Id'][i]) +'/edit'
promo_link_df = pd.DataFrame.from_dict(promo_link, orient='index', columns = ['promo_link'])
promo_link_batch_0 = promo_link_df
df.head()


# In[21]:


promo_link = {}
for i in range(0,len(df)):
    promo_link[i] = 'xxxxxxxxx'+ str(df['Id'][i]) +'/edit'
promo_link_df = pd.DataFrame.from_dict(promo_link, orient='index', columns = ['promo_link'])

df_van = {}  
for i in range(0,len(df)):
    if "van" in df['Vehicles'][i]:
        df_van[i] = 1
    else:
        df_van[i] = 0
df_van = pd.DataFrame.from_dict(df_van, orient='index', columns = ['is_van'])
        
df_motorcycle = {}  
for i in range(0,len(df)):
    if "motorcycle" in df['Vehicles'][i]:
        df_motorcycle[i] = 1
    else:
        df_motorcycle[i] = 0
df_motorcycle = pd.DataFrame.from_dict(df_motorcycle, orient='index', columns = ['is_motorcycle'])
        
df_struck = {}  
for i in range(0,len(df)):
    if "struck" in df['Vehicles'][i]:
        df_struck[i] = 1
    else:
        df_struck[i] = 0
df_struck = pd.DataFrame.from_dict(df_struck, orient='index', columns = ['is_struck'])
                
df_mtruck = {}  
for i in range(0,len(df)):
    if "mtruck" in df['Vehicles'][i]:
        df_mtruck[i] = 1
    else:
        df_mtruck[i] = 0
df_mtruck = pd.DataFrame.from_dict(df_mtruck, orient='index', columns = ['is_mtruck'])

dff = pd.concat([df, df_van, df_motorcycle, df_struck, df_mtruck, promo_link_df],axis = 1)
dff = dff[dff['Ends at'].notnull()]
dff = dff.reset_index()
 
promo_link_batch_0 = dff

'''
promo_link_batch_1 = dff[100:199]
promo_link_batch_2 = dff[200:299]
promo_link_batch_3 = dff[300:399]
promo_link_batch_4 = dff[400:499]
promo_link_batch_5 = dff[500:599]
promo_link_batch_6 = dff[600:699]
promo_link_batch_7 = dff[700:799]
promo_link_batch_8 = dff[800:899]
promo_link_batch_9 = dff[900:999]
promo_link_batch_10 = dff[1000:]
'''

dff.head()


# In[20]:


browser_0 = webdriver.Chrome(executable_path='xxxxxx')
'''
browser_1 = webdriver.Chrome(executable_path='xxxxxx')
browser_2 = webdriver.Chrome(executable_path='xxxxxx')
browser_3 = webdriver.Chrome(executable_path='xxxxxx')
browser_4 = webdriver.Chrome(executable_path='xxxxxx')
browser_5 = webdriver.Chrome(executable_path='xxxxxx')
browser_6 = webdriver.Chrome(executable_path='xxxxxx')
browser_7 = webdriver.Chrome(executable_path='xxxxxx')
browser_8 = webdriver.Chrome(executable_path='xxxxxx')
browser_9 = webdriver.Chrome(executable_path='xxxxxx')
'''


browser_0.get('xxxxxxx')
browser_0.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_0.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_0.find_element_by_id("admin_user_submit_action").click()

'''
browser_1.get('xxxxxx')
browser_1.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_1.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_1.find_element_by_id("admin_user_submit_action").click()

browser_2.get('xxxxx')
browser_2.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_2.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_2.find_element_by_id("admin_user_submit_action").click()

browser_3.get('xxxxxx')
browser_3.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_3.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_3.find_element_by_id("admin_user_submit_action").click()

browser_4.get('xxxxxx')
browser_4.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_4.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_4.find_element_by_id("admin_user_submit_action").click()

browser_5.get('xxxxxxx')
browser_5.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_5.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_5.find_element_by_id("admin_user_submit_action").click()

browser_6.get('xxxxxx')
browser_6.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_6.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_6.find_element_by_id("admin_user_submit_action").click()

browser_7.get('xxxxxx')
browser_7.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_7.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_7.find_element_by_id("admin_user_submit_action").click()

browser_8.get('xxxxxx')
browser_8.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_8.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_8.find_element_by_id("admin_user_submit_action").click()

browser_9.get('xxxxxxx')
browser_9.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_9.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_9.find_element_by_id("admin_user_submit_action").click()
'''


# for i in range(0,1):
for i in range(0,len(promo_link_batch_0)):
    
    # Step 1 : Open Parallel Crawler 
        
    browser_0.get(promo_link_batch_0['promo_link'][i])
    
    '''
    browser_1.get(promo_link_batch_1['promo_link'][100+i])
    browser_2.get(promo_link_batch_2['promo_link'][200+i])
    browser_3.get(promo_link_batch_3['promo_link'][300+i])
    browser_4.get(promo_link_batch_4['promo_link'][400+i])
    browser_5.get(promo_link_batch_5['promo_link'][500+i])
    browser_6.get(promo_link_batch_6['promo_link'][600+i])
    browser_7.get(promo_link_batch_7['promo_link'][700+i])
    browser_8.get(promo_link_batch_8['promo_link'][800+i])
    browser_9.get(promo_link_batch_9['promo_link'][900+i])
    '''

             
    # Step 2 : Tick every vehicle types + Clear End Date + Submit
    """   
    if dff['is_van'][i] == 1:
        print('VAN Checked')
    else:
        browser_0.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_0.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][i] == 1:
        print('STRUCK Checked')
    else:
        browser_0.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][i] == 1:
        print('MTRUCK Checked')
    else:
        browser_0.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')
    """ 
    #browser_0.find_element_by_xpath('//*[@id="promo_code_code"]').clear()
    #browser_0.find_element_by_xpath('//*[@id="promo_code_code"]').send_keys(int(df['new code'][i]))
    
    
    browser_0.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[7]').click()
    browser_0.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[6]').click()
    browser_0.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[32]').click()
    browser_0.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[25]').click()
    browser_0.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[61]').click()
    print('end at time reset')
        
    browser_0.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit
    
    '''
    ##1
        
    if dff['is_van'][100+i] == 1:
        print('VAN Checked')
    else:
        browser_1.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][100+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_1.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][100+i] == 1:
        print('STRUCK Checked')
    else:
        browser_1.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][100+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_1.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_1.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_1.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_1.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_1.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_1.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_1.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit
        
    ##2
        
    if dff['is_van'][200+i] == 1:
        print('VAN Checked')
    else:
        browser_2.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][200+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_2.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][200+i] == 1:
        print('STRUCK Checked')
    else:
        browser_2.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][200+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_2.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_2.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_2.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_2.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_2.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_2.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_2.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit        
        
    ##3
        
    if dff['is_van'][300+i] == 1:
        print('VAN Checked')
    else:
        browser_3.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][300+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_3.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][300+i] == 1:
        print('STRUCK Checked')
    else:
        browser_3.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][300+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_3.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_3.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_3.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_3.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_3.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_3.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_3.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit                
        
    ##4
        
    if dff['is_van'][400+i] == 1:
        print('VAN Checked')
    else:
        browser_4.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][400+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_4.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][400+i] == 1:
        print('STRUCK Checked')
    else:
        browser_4.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][400+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_4.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_4.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_4.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_4.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_4.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_4.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_4.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit                        
        
    ##5
        
    if dff['is_van'][500+i] == 1:
        print('VAN Checked')
    else:
        browser_5.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][500+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_5.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][500+i] == 1:
        print('STRUCK Checked')
    else:
        browser_5.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][500+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_5.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_5.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_5.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_5.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_5.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_5.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_5.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit                        
        
    ##6
        
    if dff['is_van'][600+i] == 1:
        print('VAN Checked')
    else:
        browser_6.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][600+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_6.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][600+i] == 1:
        print('STRUCK Checked')
    else:
        browser_6.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][600+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_6.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_6.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_6.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_6.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_6.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_6.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_6.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit                        
        
    ##7
        
    if dff['is_van'][700+i] == 1:
        print('VAN Checked')
    else:
        browser_7.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][700+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_7.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][700+i] == 1:
        print('STRUCK Checked')
    else:
        browser_7.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][700+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_7.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_7.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_7.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_7.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_7.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_7.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_7.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit                        
        
    ##8
        
    if dff['is_van'][800+i] == 1:
        print('VAN Checked')
    else:
        browser_8.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][800+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_8.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][800+i] == 1:
        print('STRUCK Checked')
    else:
        browser_8.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][800+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_8.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_8.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_8.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_8.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_8.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_8.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_8.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit                  
        
    ##9
        
    if dff['is_van'][900+i] == 1:
        print('VAN Checked')
    else:
        browser_9.find_element_by_id('promo_code_vehicles_van').click()
        print('VAN Re-checked')
        
    if dff['is_motorcycle'][900+i] == 1:
        print('MOTORCYCLE Checked')
    else:
        browser_9.find_element_by_id('promo_code_vehicles_motorcycle').click()
        print('MOTORCYCLE Re-checked')
        
    if dff['is_struck'][900+i] == 1:
        print('STRUCK Checked')
    else:
        browser_9.find_element_by_id('promo_code_vehicles_struck').click()
        print('STRUCK Re-checked')
        
    if dff['is_mtruck'][900+i] == 1:
        print('MTRUCK Checked')
    else:
        browser_9.find_element_by_id('promo_code_vehicles_mtruck').click()
        print('MTRUCK Re-checked')

    browser_9.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
    browser_9.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
    browser_9.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
    browser_9.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
    browser_9.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
    print('end at time reset')
        
    browser_9.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit  
    '''


# In[9]:


browser_10 = webdriver.Chrome(executable_path='xxxxxx')
browser_10.get('xxxx')
browser_10.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser_10.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser_10.find_element_by_id("admin_user_submit_action").click()

for i in range(0,len(promo_link_batch_10)):
    browser_10.get(promo_link_batch_10['promo_link'][1000+i])
            
    ##10
    try:
        if dff['is_van'][1000+i] == 1:
            print('VAN Checked')
        else:
            browser_10.find_element_by_id('promo_code_vehicles_van').click()
            print('VAN Re-checked')
        
        if dff['is_motorcycle'][1000+i] == 1:
            print('MOTORCYCLE Checked')
        else:
            browser_10.find_element_by_id('promo_code_vehicles_motorcycle').click()
            print('MOTORCYCLE Re-checked')
        
        if dff['is_struck'][1000+i] == 1:
            print('STRUCK Checked')
        else:
            browser_10.find_element_by_id('promo_code_vehicles_struck').click()
            print('STRUCK Re-checked')
        
        if dff['is_mtruck'][1000+i] == 1:
            print('MTRUCK Checked')
        else:
            browser_10.find_element_by_id('promo_code_vehicles_mtruck').click()
            print('MTRUCK Re-checked')

        browser_10.find_element_by_xpath('//*[@id="promo_code_ends_at_1i"]/option[1]').click()
        browser_10.find_element_by_xpath('//*[@id="promo_code_ends_at_2i"]/option[1]').click()
        browser_10.find_element_by_xpath('//*[@id="promo_code_ends_at_3i"]/option[1]').click()
        browser_10.find_element_by_xpath('//*[@id="promo_code_ends_at_4i"]/option[1]').click()
        browser_10.find_element_by_xpath('//*[@id="promo_code_ends_at_5i"]/option[1]').click()
        print('end at time reset')
        
        browser_10.find_element_by_xpath('//*[@id="promo_code_submit_action"]/input').click() # submit                                  
         
    except:
        browser_10.close()
   


# In[ ]:




