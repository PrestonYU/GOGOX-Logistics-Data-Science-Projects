#!/usr/bin/env python
# coding: utf-8

# # Semi-Auto Mode 半自動模式

# In[181]:


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
import json
import base64

# Load Google Spreadsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

Admin_User_Email = str('xxxxxxxx')
Admin_User_Password = str('xxxxxxxx')
SCROLL_PAUSE_TIME = 1
Admin_User_Email2 = str('xxxxxxx')
Admin_User_Password2 = str('xxxxxxxx')

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
google_key_file = 'xxxxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

workbook = gc.open_by_key('xxxxxxxxxxxxxxx')
sheet = workbook.worksheet('Ready_to_Dispatch')
wks_name = 'Ready_to_Dispatch'

browser = webdriver.Chrome(executable_path='xxxxxxxxxx')
browser.get('xxxxxxxxxx')
time.sleep(2)
browser.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

browser2 = webdriver.Chrome(executable_path='xxxxxxxxxx')
browser2.get('https://app.intercom.com/xxxxxxxxxxxx:' + b64code)
time.sleep(5)
browser2.find_element_by_xpath('//*[@id="admin_email"]').send_keys(Admin_User_Email2)
browser2.find_element_by_xpath('//*[@id="admin_password"]').send_keys(Admin_User_Password2)
browser2.find_element_by_xpath('//*[@id="new_admin"]/div[11]/button').click()


time.sleep(30)
while True:
    values = sheet.get_all_values()
    df = pd.DataFrame(values[:], columns = values[0])
    df = df[1:]
    df = df.reset_index(drop = True)
    time.sleep(3)

    for i in range(0,len(df)):
    
        try:
            browser.get('xxxxxxxxxxx')
    
            browser.find_element_by_xpath('//*[@id="order_order_request_id"]').send_keys(df['訂單編號'][i])
            browser.find_element_by_xpath('//*[@id="order_driver_id"]').send_keys(df['指派司機'][i])
            browser.find_element_by_xpath('//*[@id="order_submit_action"]/input').click()
            
            
            n = df['指派司機'][i]
            code = {"predicates":[{"comparison":"eq","value": 'TW' + str(n.zfill(9))  ,"attribute":"user_id","type":"string"},{"type":"role","attribute":"role","comparison":"eq","value":"user_role"}]}
            code = json.dumps(code)
            code = code.replace(' ','')
            b64code = base64.b64encode(code.encode("utf-8")).decode('utf-8')
            
            
            browser2.get('https://app.intercom.com/xxxxxxxxx:' + b64code)
            time.sleep(5)
            
            browser2.find_element_by_id('ember688').click()
            browser2.find_element_by_id('ember757').clear()
            browser2.find_element_by_id('ember757').send_keys('⚠️系統已自動分派訂單編號： ' + df['訂單編號'][i] + '給您，請至【我的訂單】查看進行中的訂單。')
            browser2.find_element_by_id('ember791').click()
            time.sleep(2)
            pass
    
        except:
            time.sleep(2)
            continue
            
    time.sleep(5)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Auto Mode 全自動模式  

# In[84]:


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
import json
import base64

# Load Google Spreadsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

Admin_User_Email = str('xxxxxxx')
Admin_User_Password = str('xxxxxxxxxxx')
SCROLL_PAUSE_TIME = 1
Admin_User_Email2 = str('xxxxxxx')
Admin_User_Password2 = str('xxxxxxxxx')

browser = webdriver.Chrome(executable_path='xxxxxxx')
browser.get('xxxxxxxxxx')



# In[ ]:


browser1 = webdriver.Chrome(executable_path='xxxxxxxxxx')
browser1.get('xxxxxxxx')
time.sleep(3)
browser1.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
browser1.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
browser1.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

browser2 = webdriver.Chrome(executable_path='xxxxxxx')
browser2.get('https://app.intercom.com/a/xxxxxxxxx:' + b64code)
time.sleep(5)
browser2.find_element_by_xpath('//*[@id="admin_email"]').send_keys(Admin_User_Email2)
browser2.find_element_by_xpath('//*[@id="admin_password"]').send_keys(Admin_User_Password2)
browser2.find_element_by_xpath('//*[@id="new_admin"]/div[11]/button').click()


# In[85]:


import glob
import os
pd.options.display.float_format = '{:.0f}'.format

while True:

# ==============================
# ======== DOWNLOAD CSV ========
# ==============================
    try:
        browser.find_element_by_xpath('//*[@id="slice_5978-controls"]/div').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="GRID_ID-pane-0"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div/ul/li[8]').click()
        pass
    
    except:
        continue

# =================================
# ======== CSV ARRANGEMENT ========
# =================================

    list_of_files = glob.glob('*.csv') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    dff = pd.read_csv(latest_file,index_col = False)

    columns = ['order_request_id','dispatch_driver']
    drf = pd.DataFrame(columns = columns)


    for i in range(0,len(dff['order_request_id'].unique())):
    
        a = dff[(dff['order_request_id'] == dff['order_request_id'].unique()[i]) & (dff['ordinary_dispatch'].notnull())]
        b = dff[(dff['order_request_id'] == dff['order_request_id'].unique()[i]) & (dff['forward_dispatch'].notnull())]
        c = dff[(dff['order_request_id'] == dff['order_request_id'].unique()[i]) & (dff['order_consolidation_dispatch'].notnull())]
        d = dff[(dff['order_request_id'] == dff['order_request_id'].unique()[i]) & (dff['broadcast_dispatch'].notnull())]
    
        a = a.reset_index(drop = True)
        b = b.reset_index(drop = True)
        c = c.reset_index(drop = True)
        d = d.reset_index(drop = True)
    
    
        if len(a) > 0:
            if len(a[a['ordinary_dispatch'] != a['release_driver_id']]) > 0:
                a1 = a[a['ordinary_dispatch'] != a['release_driver_id']]
                a1 = a1.reset_index(drop = True)
                dd1 = a1[['order_request_id','ordinary_dispatch']] 
                dd1.columns = columns
                drf = drf.append(dd1,ignore_index = True) 
        else:
            pass
        
        if len(b) > 0:
            if len(b[b['forward_dispatch'] != b['release_driver_id']]) > 0:
                b1 = b[b['forward_dispatch'] != b['release_driver_id']]
                b1 = b1.reset_index(drop = True)
                dd2 = b1[['order_request_id','forward_dispatch']] 
                dd2.columns = columns
                drf = drf.append(dd2,ignore_index = True) 
        else:
            pass
    
        if len(c) > 0:
            if len(c[c['order_consolidation_dispatch'] != c['release_driver_id']]) > 0:
                c1 = c[c['order_consolidation_dispatch'] != c['release_driver_id']]
                c1 = c1.reset_index(drop = True)
                dd3 = c1[['order_request_id','order_consolidation_dispatch']]
                dd3.columns = columns
                drf = drf.append(dd3,ignore_index = True)
        else:
            pass
    
        if len(d) > 0:
            if len(d[d['broadcast_dispatch'] != d['release_driver_id']]) > 0:
                d1 = d[d['broadcast_dispatch'] != d['release_driver_id']]
                d1 = d1.reset_index(drop = True)
                dd4 = d1[['order_request_id','broadcast_dispatch']]
                dd4.columns = columns
                drf = drf.append(dd4,ignore_index = True)
        else:
            continue

    drf = drf.reset_index()
    drf['rank'] = drf.groupby('order_request_id')['index'].rank("dense", ascending = True)
    dkf = drf[drf['rank'] == 1]
    dkf = dkf.reset_index(drop = True)


# ======================
# ======== LOOP ========
# ======================

    for i in range(0,len(dkf)):
    
        try:
            browser1.get('xxxxxxxxxx')
    
            browser1.find_element_by_xpath('//*[@id="order_order_request_id"]').send_keys(int(dkf['order_request_id'][i]))
            browser1.find_element_by_xpath('//*[@id="order_driver_id"]').send_keys(int(dkf['dispatch_driver'][i]))
            browser1.find_element_by_xpath('//*[@id="order_submit_action"]/input').click()
            
            n = int(dkf['dispatch_driver'][i])
            code = {"predicates":[{"comparison":"eq","value": 'TW' + str(n.zfill(9))  ,"attribute":"user_id","type":"string"},{"type":"role","attribute":"role","comparison":"eq","value":"user_role"}]}
            code = json.dumps(code)
            code = code.replace(' ','')
            b64code = base64.b64encode(code.encode("utf-8")).decode('utf-8')
            
            
            browser2.get('https://app.intercom.com/a/xxxxxxxxxx' + b64code)
            time.sleep(5)
            browser2.find_element_by_id('ember688').click()
            browser2.find_element_by_id('ember757').clear()
            browser2.find_element_by_id('ember757').send_keys('⚠️系統已自動分派訂單編號： ' + int(dkf['order_request_id'][i]) + '給您，請至【我的訂單】查看進行中的訂單。')
            browser2.find_element_by_id('ember791').click()
            time.sleep(2)
        
        except:
            time.sleep(2)
            continue

        
# ============================================
# ======== REMOVE REDUNDANT CSV FILES ========
# ============================================
    
    for i in range(0,len(list_of_files)):
        os.remove(list_of_files[i])

    time.sleep(5)

