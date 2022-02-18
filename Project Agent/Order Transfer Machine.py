#!/usr/bin/env python
# coding: utf-8

# In[148]:


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

# Load Google Spreadsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

Admin_User_Email = str('xxxxxxxx')
Admin_User_Password = str('xxxxxxxx')
SCROLL_PAUSE_TIME = 1

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
google_key_file = 'xxxxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

workbook = gc.open_by_key('xxxxxxxx')
sheet = workbook.worksheet('Order_Master')
sheet2 = workbook.worksheet('Job_Done')
wks_name = 'Job_Done'

while True:
    time.sleep(2)
    values = sheet.get_all_values()
    df = pd.DataFrame(values[:], columns = values[0])
    df = df[1:]
    df = df[df['Job'] == '']
    df = df.reset_index(drop = True)
    
    if len(df) < 1:
        time.sleep(10)
        continue
    
    elif len(df) > 0:
        for i in range(0,len(df)):
            browser = webdriver.Chrome(executable_path='xxxxxxxx')
            browser.get('xxxxxxxx' + df['單號'][i])
            browser.find_element_by_id("admin_user_email").send_keys(Admin_User_Email)
            browser.find_element_by_id("admin_user_password").send_keys(Admin_User_Password)
            browser.find_element_by_xpath('//*[@id="admin_user_submit_action"]/input').click()

            
# Check1 : 檢查該訂單是否允許修改價格，限定有特殊Additional Requirement才可以修改價格
            last_height = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            while True:
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            html = browser.page_source
            soup = BeautifulSoup(html,"lxml")
            group_block = soup.find_all('tr',attrs={'class':'row row-new_breakdown'})
            for j, group_item in enumerate(group_block):
                group_url = group_item.find('td')
            if '0_test3' not in group_url.string and '0_test4' not in group_url.string: # insert additional requirement by adding "and" operator
                print("check1 - order type match - deny")
                df['Job'][i] = 'Deny - Disqualified Order'
                time.sleep(2)
                browser.close()
                continue
            else:
                print("check1 - order type match - pass")
                time.sleep(2)
                
                
                browser.get('xxxxxxxxxxxxx' + df['單號'][i] + '&commit=Filter&order=id_desc')
                last_height = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                while True:
                    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                html = browser.page_source
                soup = BeautifulSoup(html,"lxml")
                group_block = soup.find_all('td',attrs={'class':'col col-driver'})
                for j, group_item in enumerate(group_block):
                    group_url = group_item.find('a')["href"]
                    driver_url = "xxxxxxxxx" + str(group_url) 
    
                current_driver_url = 'xxxxxxxxxxx' + df['目前承接司機'][i]
        
# Check2 : 檢查是否為當前承接司機
                if current_driver_url != driver_url: 
                    print("check2 - original driver match - deny")
                    df['Job'][i] = 'Deny - Driver Mismatch'
                    time.sleep(2)
                    browser.close()
                    continue
                else:
                    print("check2 - original driver match - pass")
                    group_block = soup.find_all('td',attrs={'class':'col col-id'})
                    for j, group_item in enumerate(group_block):
                        group_url = group_item.find('a')["href"]
                        order_url = "xxxxxxxx" + str(group_url) + "/edit"
        
# Check3 : 檢查移轉目標對象是否有足夠Credits 
                    if df['指派司機(非必填)'][i] != '':
                        browser.get('xxxxxxxxx'+ df['指派司機(非必填)'][i] + '&commit=Filter&order=id_desc')
                        
                    else:
                        browser.get('xxxxxxxx'+ df['目前承接司機'][i] + '&commit=Filter&order=id_desc')
                        
                        
                    last_height = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                    while True:
                        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                        time.sleep(SCROLL_PAUSE_TIME)
                        new_height = browser.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height

                    html = browser.page_source
                    soup = BeautifulSoup(html,"lxml")
                    group_block = soup.find_all('td',attrs={'class':'col col-credits'})
                    credits = float(group_block[0].string)
                    new_coin_price = int(df['調整報價'][i]) - round(int(df['調整報價'][i])*0.82)
    
                    if credits <= new_coin_price + 200:
                        print("check3 - enough credit - deny")
                        df['Job'][i] = 'Deny - No Credits'
                        time.sleep(2)
                        browser.close()
                        continue
                    else:
                        print("check3 - enough credit - pass")

##### Price Amendment #####

                        browser.get('xxxxxxxxx' + df['單號'][i] + '/edit')
                        time.sleep(2)
                        browser.find_element_by_id("order_request_price_incl_vat").clear()
                        browser.find_element_by_id("order_request_price_incl_vat").send_keys(df['調整報價'][i])
                        browser.find_element_by_id("order_request_price_ex").clear()
                        browser.find_element_by_id("order_request_price_ex").send_keys(df['調整報價'][i])
                        browser.find_element_by_id("order_request_customer_price").clear()
                        browser.find_element_by_id("order_request_customer_price").send_keys(df['調整報價'][i])
                        browser.find_element_by_xpath('//*[@id="order_request_submit_action"]/input').click()
                        time.sleep(5)

##### Order Transferring #####                        
   
                        if df['指派司機(非必填)'][i] != '':
                            browser.get(order_url)
                            time.sleep(2)
                            browser.find_element_by_id("order_driver_id").clear()
                            browser.find_element_by_id("order_driver_id").send_keys(df['指派司機(非必填)'][0])
                            browser.find_element_by_xpath('//*[@id="order_submit_action"]/input').click()
                            time.sleep(5)
                            
                        else:
                            time.sleep(5)
                            

##### GOGOCoin Adjustment #####

                        browser.get('xxxxxxxxx' + df['單號'][i])
                        last_height = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                        while True:
                            browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                            time.sleep(SCROLL_PAUSE_TIME)
                            new_height = browser.execute_script("return document.body.scrollHeight")
                            if new_height == last_height:
                                break
                            last_height = new_height

                        html = browser.page_source
                        soup = BeautifulSoup(html,"lxml")
                        group_block = soup.find_all('tr',attrs={'class':'row row-coin_price'})
                        for j, group_item in enumerate(group_block):
                            coin_price = group_item.find('td')
                        coin_price = float(coin_price.string)
        
                        if df['指派司機(非必填)'][i] != '':
                            browser.get('xxxxxxxx'+ df['指派司機(非必填)'][i] +'/edit')
                            
                        else: 
                            browser.get('xxxxxxxx'+ df['目前承接司機'][i] +'/edit')
                            
                            
                        time.sleep(2)
                        browser.find_element_by_xpath('//*[@id="add-minus-non-withdrawable-credits-button"]').click()
                        time.sleep(5)
                        new_coin_price = int(df['調整報價'][i]) - round(int(df['調整報價'][i])*0.82)
                        browser.find_element_by_xpath('//*[@id="non-withdrawable-credits"]').send_keys(str(coin_price - new_coin_price))
                        browser.find_element_by_xpath('//*[@id="reason-text"]').send_keys('Order_Transfer')
                        browser.find_element_by_xpath('//*[@id="order-request-id"]').send_keys(df['單號'][i])
                        time.sleep(5)
                        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/button[1]').click()
                        try:
                            browser.switch_to.alert.accept() 
                        except:
                            continue
                        time.sleep(2)
                        # browser.find_element_by_xpath('//*[@id="driver_submit_action"]/input').click()
                        print('transfer done')

                        df['Job'][i] = 'Done'
                        time.sleep(2)
                        browser.close()
                        
                        continue
                        
        values2 = sheet2.get_all_values()
        done_df = pd.DataFrame(values2[:], columns = values2[0])
        done_df = done_df.iloc[1:,1:]
        done_df = done_df.reset_index(drop = True)
        upload_df = pd.concat([done_df,df], ignore_index=True)
        upload_df = upload_df .reset_index(drop = True)

        d2g.upload(upload_df, 'xxxxxxxxx', wks_name, credentials=credentials, clean = True)
        print('upload done')
        time.sleep(10)
            
        continue


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




