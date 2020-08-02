#!/usr/bin/env python
# coding: utf-8

# In[156]:


import selenium
from selenium.webdriver import ActionChains


# In[157]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import os
import bs4
import time
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np
from pymongo import MongoClient
import urllib 
import dns


# In[158]:


options = Options()
options.add_argument("start-maximized")#fullscreen mode
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
def patching_get(driver, url):
    # Run this until works
    done = False
    tries = 10
    x = 0
    while not done:
        x += 1
        if x > tries:
            raise
        try:
            driver.get(url)
            done = True
        except KeyboardInterrupt:
            raise
        except: 
            time.sleep(1)
    return driver


# In[159]:


def login(driver,start_url = "https://in.pinterest.com/",email = "kbhardwaj085@gmail.com",password = "Avik@838"):
    try:
        driver = patching_get(driver,start_url)
        time.sleep(10)
    except Exception as e:
        print(e)
        raise(e)
    login = driver.find_element_by_class_name('tg7')
    try:
        login.click()
    except Exception as e:
        print(e)
        raise(e)
    email_box = driver.find_element_by_id('email')
    try:
        time.sleep(2)
        email_box.send_keys('a')
        email_box.send_keys('v')
        email_box.send_keys('i')
        email_box.send_keys('k')
        email_box.send_keys('p')
        email_box.send_keys('a')
        email_box.send_keys('n')
        email_box.send_keys('d')
        email_box.send_keys('e')
        email_box.send_keys('y')
        email_box.send_keys('1')
        email_box.send_keys('@')
        email_box.send_keys('g')
        email_box.send_keys('m')
        email_box.send_keys('a')
        email_box.send_keys('i')
        email_box.send_keys('l')
        email_box.send_keys('.')
        email_box.send_keys('c')
        email_box.send_keys('o')
        email_box.send_keys('m')
    except Exception as e:
        print(e)
        raise(e)
    password_box = driver.find_element_by_id('password')
    try:
        time.sleep(2)
        password_box.send_keys('A')
        password_box.send_keys('v')
        password_box.send_keys('i')
        password_box.send_keys('k')
        password_box.send_keys('@')
        password_box.send_keys('8')
        password_box.send_keys('3')
        password_box.send_keys('8')
    except Exception as e:
        print(e)
        raise(e)    
    signUp = driver.find_element_by_class_name('SignupButton')
#     signUp.click()
    try:
        
        password_box.send_keys(Keys.ENTER)
        time.sleep(5)
    except Exception as e:
        print(e)
        raise(e)
    
        

imgLinks = []
def set_model(driver,model = "kendall jenner outfits",start_url = "https://in.pinterest.com/"):
    try:
        login(driver,email = "avikpandey1@gmail.com",password = "Avik@838")
    except Exception as e:
        print(e)
        raise(e)
    try:    
        time.sleep(3)
        search_box = driver.find_element_by_tag_name('input')
        time.sleep(4)
        search_box = driver.find_element_by_tag_name('input')
        time.sleep(2)
    except Exception as e:
        print(e)
        raise(e)
    try:
        
        search_box.send_keys(model)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
#         search_box.send_keys(Keys.ENTER)
        time.sleep(3)
    except Exception as e: 
        print(e)
#         set_location(driver, location='bangalore', pincode = "560103", start_url = "https://www.bigbasket.com/")
        raise(e)
    myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.TAG_NAME,"img"))))
#             images = driver.find_elements_by_tag_name('img')
    images = []
    final = []
    while True: 
        driver.execute_script("window.scrollBy(0,1200)", "")
        try:
            WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_tag_name("img")) > myLength)
            images = driver.find_elements_by_tag_name("img")
            time.sleep(3)
            for el in images:
                time.sleep(1)
                link = el.get_attribute('src')
                time.sleep(1)
                link = el.get_attribute('src')
                final.append(link)
                
            myLength = len(images)
        except TimeoutException:
            break
    print(len(images))
                
#     images = driver.find_elements_by_tag_name('img')
#     print(len(images))
    cnt = 0
    print(len(final))
    for i in range(len(final)):
        if i == 0:
            continue
        print(final[i])
        print(i)
        max_attemps = 10
#         ok=""
#         while True:
#             ok = images[i].get_attribute("src")

#             if ok is not None:

#                 break
#             else:
#                 time.sleep(0.5)
#             max_attemps -= 1

#             if max_attemps == 0:
#                 print("Cannot find element.")
#         try:
#             time.sleep(4)
#             imgLink = images[i].get_attribute('src')
#             time.sleep(2)
#             imgLink = images[i].get_attribute('src')
#         except StaleElementReferenceException as e:
#             print(e)
#             raise(e)
            
        fin = {'model' : model
            ,'img-url' : final[i]}    
        print(next)
        imgLinks.append(fin)
     
    driver.quit()
    return imgLinks
    
    
    


# In[160]:


set_model(driver,model = "kendall jenner outfits")


# In[161]:


client = MongoClient('mongodb+srv://user:'+urllib.parse.quote('flipkart')+'@cluster0.pe7lw.mongodb.net/intelFashion?retryWrites=true&w=majority')
print(client)
db = client['intelFashion']
pinterestImg = db.pinterest
print(pinterestImg)
pinterestImg.remove()
result = pinterestImg.insert_many(imgLinks)
for object_id in result.inserted_ids:
    print(str(object_id))


# In[ ]:




