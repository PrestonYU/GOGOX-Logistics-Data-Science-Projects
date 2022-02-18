#!/usr/bin/env python
# coding: utf-8

# In[7]:


# import selenium chromedriver
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
browser = webdriver.Chrome(executable_path='/Applications/Google Chrome.app/Contents/MacOS/chromedriver')
browser.get("xxxxxxxxx")


# In[ ]:


# Manually Insert the authentication info
# Username: xxxxxx
# Password: xxxxxxx

# Then Login with Google Account


# In[5]:


while True:
    browser.find_element_by_xpath('//*[@id="js-sql-toolbar"]/div[1]/form/span[1]/button').click()
    time.sleep(30)   
    browser.find_element_by_link_text('.CSV').click()
    time.sleep(25)  
    import pandas as pd 
    import warnings
    warnings.filterwarnings("ignore")
    
    # Backend Setting : https://console.developers.xxxxxxxxxxx
    # Connect to Google Sheet
    import gspread 
    from oauth2client.service_account import ServiceAccountCredentials
    from df2gspread import df2gspread as d2g
    
    # Configure the connection
    scope = ['https://spreadsheets.google.com/feeds']
    
    # Give the path to the Service Account Credential 
    credentials = ServiceAccountCredentials.from_json_keyfile_name('xxxxxxxxx')
    
    # Authorize Jupyter Notebook
    gc = gspread.authorize(credentials)
    
    # The gsheet ID
    # Sheet URL : https://docs.google.com/spreadsheets/d/xxxxxxxxxxx
    spreadsheet_key = 'xxxxxxx'
    
    # Read CSV
    import glob
    import os
    list_of_files = glob.glob('*.csv') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    df = pd.read_csv(latest_file,index_col = False)
    
    # Set the sheet name for uploading the dataframe
    wks_name = 'Driver Current Location'
    cell_of_start_df = 'A1'
    
    # Upload the dataframe
    d2g.upload(df,
               spreadsheet_key,
               wks_name,
               credentials = credentials,
               start_cell = cell_of_start_df,
               clean = True)
    
    time.sleep(10)


# In[ ]:





# In[ ]:




