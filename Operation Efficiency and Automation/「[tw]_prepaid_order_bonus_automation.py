# -*- coding: utf-8 -*-
"""「[TW] Prepaid Order Bonus Automation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/xxxxxxxxxx

# Setting
"""

#install chromium, its driver, selenium and other packages:
#!apt install chromium-chromedriver
#!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

!pip install google-auth
!pip install selenium
!pip install requests
!pip install bs4
!pip install lxml
!pip install --upgrade -q gspread
!pip install gspread_dataframe

# Set Admin Panel Login Account and Password
Admin_User_Email = str('xxxxxx')
Admin_User_Password = str('xxxxxxxxxx')

# Grant Google Access 
import os                                                                       # Mount the drive from Google to save the dataset
from google.colab import drive                                                  # this will be our driver
drive.mount('/gdrive')
root = '/gdrive/My Drive/'

from google.colab import auth
auth.authenticate_user()

import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(GoogleCredentials.get_application_default())

"""# Web Crawler Automation"""

import time
from datetime import datetime, timedelta


# Loop  
while True:
  
  #set options to be headless
  from selenium import webdriver
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  d = webdriver.Chrome(chrome_options=chrome_options)
  
  import datetime
  # Insert Target Site
  bonus_start_time = datetime.date.today().strftime("%Y-%m-%d+") + '00%3A00'
  bonus_end_time = datetime.date.today().strftime("%Y-%m-%d+") + '23%3A59'
  # d.get('xxxxxxx')    
  d.get('xxxxx')           
  d.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)            # Admin User Email
  d.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)      # Admin User Password
  #d.find_element_by_id("admin_user_submit_action").click()
  d.find_element_by_name("commit").click()
  
  try:
    # Download Table
    from selenium.webdriver import ActionChains
    d.find_element_by_xpath("//*[@id='index_footer']/div[2]/a[1]").click()
    time.sleep(15)

    import os 
    os.rename('/content/order-requests-' + time.strftime("%Y-%m-%d", time.localtime()) + '.csv','add_bonus.csv')

    # Import Table to Readable DataFrame
    import pandas as pd 
    import time
    download_table = pd.read_csv('add_bonus.csv')
    download_table = download_table[download_table['Company bonus'].isna()]
    
    # Double Insurances
    download_table = download_table[download_table['Vehicle'] == 'motorcycle']
    download_table = download_table[download_table['Status'] == 'pending']
    #download_table = download_table[download_table['Company bonus'] < 50]  
    download_table = download_table[download_table['Company bonus'].isna()]  
    download_table = download_table[download_table['Organization'] == 'foodomo']

    new_download_table = download_table[download_table['客人名稱'].str.contains('STARBUCKS') == 1] 
    download_table = download_table[download_table['客人名稱'].str.contains('STARBUCKS') == 0] 
    #download_table = download_table[(download_table['Created at'] >= datetime.date.today().strftime("%Y-%m-%d 06:00:00")) & (download_table['Created at'] <= datetime.date.today().strftime("%Y-%m-%d 23:00:00")) ]
    download_table = download_table.reset_index(drop = True)
    new_download_table = new_download_table.reset_index(drop = True)

    # Generate Detail Page URL
    order_link = {}
    for i in range(0,len(download_table)):
      order_link[i] = 'xxxxx' + str(download_table['Id'][i]) + '/edit'
    
    # Alter Bonus (paid by GOGOVAN)
    for k in range(0,len(order_link)):
      d.get(order_link[k])
      d.find_element_by_id("order_request_company_bonus").send_keys("15")
      d.find_element_by_id("order_request_submit_action").click()


    # Generate Detail Page URL - for special case
    order_link1 = {}
    for i in range(0,len(new_download_table)):
      order_link1[i] = 'xxxxx' + str(new_download_table['Id'][i]) + '/edit'
    
    # Alter Bonus (paid by GOGOVAN) - for special case
    for k in range(0,len(order_link1)):
      d.get(order_link1[k])
      d.find_element_by_id("order_request_company_bonus").send_keys("25")
      d.find_element_by_id("order_request_submit_action").click()




    # Check if there's any pending error bug (add company bonus and pick order at the same time, the system will result in certain failure)
    download_table = pd.read_csv('add_bonus.csv')
    download_table = download_table[download_table['Vehicle'] == 'motorcycle']
    download_table = download_table[download_table['Status'] == 'pending']
    download_table = download_table[download_table['Organization'] == 'foodomo']
    download_table = download_table[download_table['Driver'].notnull()]
    download_table = download_table.reset_index(drop = True)
    
    order_link = {}
    for i in range(0,len(download_table)):
      order_link[i] = 'xxxxxx' + str(download_table['Id'][i]) + '/edit'

    for k in range(0,len(order_link)):
      d.get(order_link[k])
      #s0 = Select(d.find_element_by_id('order_request_status_cd'))
      #s0.select_by_value("2")
      d.find_element_by_xpath('//*[@id="order_request_status_cd"]/option[3]').click()
      d.find_element_by_id("order_request_submit_action").click()

    time.sleep(15)

  except: 
    time.sleep(15)

