#!/usr/bin/env python
# coding: utf-8

# In[12]:


import selenium
from selenium.webdriver import ActionChains


# In[13]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
#client = MongoClient('mongodb+srv://user:' + urllib.parse.quote('Avik@838') +' @cluster0.pe7lw.mongodb.net/intelFashion?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://user:'+urllib.parse.quote('Avik@838')+'@cluster0.pe7lw.mongodb.net/intelFashion?retryWrites=true&w=majority')
print(client)
db = client['intelFashion']
magazineImg = db.magazine
print(magazineImg)


# In[14]:


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


# In[15]:


images = []
def getImages(driver,base_url = "https://www.vogue.in"):
    driver = patching_get(driver,base_url)
    print("yeha")
    time.sleep(1);
    ele = driver.find_element_by_xpath('//*[@id="app-root"]/section/div[2]/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/a[1]')
    link = driver.find_element_by_xpath('//*[@id="app-root"]/section/div[2]/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/a[1]').text
    lee = ele.get_attribute('href')
    print(link,"okk")
    print(lee,"dkjak")
    try:
        ele.click()
        print('clcike')
        time.sleep(4)
        
        print('xuasx')
        
    except:
        pass
   
    base_url = lee
    print(base_url,"aska")
    driver = patching_get(driver,base_url)
    
#     ele2 = driver.find_element_by_xpath('//*[@id="app-root"]/section/main/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/a[3]')     
    try:
        print('ehy')
        url = '/fashion/fashion-trends'
        driver.find_element_by_xpath('//a[@href="'+url+'"]').click()
    except:
        pass
    new_url = base_url + '/fashion-trends'
    driver = patching_get(driver,new_url)
    
    
    condition = True
    cnt = 0
    while condition:
        cnt = cnt + 1
        myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.TAG_NAME,"img"))))
        imgLinks = []
        while True:
            driver.execute_script("window.scrollBy(0,800)", "")
            try:
                WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_tag_name("img")) > myLength)
                img_links = driver.find_elements_by_tag_name("img")
                myLength = len(img_links)
            except TimeoutException:
                break
        print(len(img_links))
        
        for el in img_links:
            name = el.get_attribute("src")
            time.sleep(0.1)
            name = el.get_attribute("src")
            fin = {
                'img_link':name
            }
            images.append(fin)
        
        nextBtn = driver.find_elements_by_class_name('bmYSpE')
        size = len(nextBtn)
        print(size)
        if size == 1 and cnt == 1:
            Btn = nextBtn[0]
            Btn.click()
        elif size == 2 :
            Btn = nextBtn[1]
            Btn.click()
            
        else:
            condition = False
        
        
    driver.quit()    
    return images
    


# In[16]:


getImages(driver)


# In[17]:


# arr = [{ 'img_link':'faka'}]
result = magazineImg.insert_many(images)
for object_id in result.inserted_ids:
    print(str(object_id))


# In[ ]:




