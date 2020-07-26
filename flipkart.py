#!/usr/bin/env python
# coding: utf-8

# In[1]:


import selenium
from selenium.webdriver import ActionChains


# In[2]:


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


# In[3]:


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


# In[4]:


allCategories = []
def getAllCategories(driver,base_url = "https://www.flipkart.com/"):
    try:    
        driver = patching_get(driver,base_url)
        menPath = driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div/ul/li[3]/span').text
        womenPath = driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div/ul/li[4]/span').text
        print(menPath)
        print(womenPath)
        links = driver.find_elements_by_class_name('_3GtRpC')
        print(len(links))
        for i in range(len(links)):
            if(i == 0 or i == 1):
                continue
            if(i > 3):
                break
            majCatName = ""
            if(i == 2):
                majCatName = menPath
            elif(i == 3):
                majCatName = womenPath
            print(links[i])
            el = links[i]
            lowCategories = el.find_elements_by_tag_name('a')
            print(len(lowCategories))
            tot = []
            allLinks = []
            for lowCat in lowCategories:
                singleLink = []
                name = lowCat.get_attribute('title')
            
                link = lowCat.get_attribute('href')
                singleLink.append(name)
                singleLink.append(link)
                allLinks.append(singleLink)
            tot.append(majCatName)
            tot.append(allLinks)
            allCategories.append(tot)
    except Exception as e:
        print(e)
        raise(e)
    return allCategories     
        
        
    print(len(links))


# In[5]:


getAllCategories(driver)


# In[6]:


allProducts = []

def getAllProducts(driver):
    for el in allCategories:
        majCatName = el[0]
        print(majCatName)
        for e in el[1]:
            secCatName = e[0]
            print(secCatName)
            driver = patching_get(driver,e[1])
            try:
                img_links = driver.find_elements_by_class_name('_1SSAGr')
            except:
                pass
            all_img_links = []
            print(len(img_links))    
            print(len(all_img_links))
            trendingInfo = []
            for image in img_links:
                imgLink = image.find_element_by_tag_name('img').get_attribute('src')
                all_img_links.append(imgLink)
                temp = False
                try:
                    tmp1=image.find_element_by_class_name("_1K7fCP") 
                    temp = True
                except NoSuchElementException:
                    temp = False
                if temp == True:
                    trendingInfo.append(temp)
                else:      
                    try:
                        tmp2=image.find_element_by_class_name('_3pAmCA')
                    except NoSuchElementException:
                        temp = False
            
                    trendingInfo.append(temp)
            print(len(all_img_links))
            productInfo = driver.find_elements_by_class_name('_2LFGJH')
            companyName = []
            moreProductInfo = []
            print(len(productInfo))
            for prod in productInfo:
                try:
                    
                    brandName = prod.find_element_by_class_name('_2B_pmu').text
                except NoSuchElementException:
                    brandName =  ""
                productName = prod.find_element_by_class_name('_2mylT6').text
                companyName.append(brandName)
                moreProductInfo.append(productName)
            
            size = len(companyName)
            
            for i in range(size):
                if len(all_img_links) == 0:
                    break
                fin = {
                    'Major-Category':majCatName,
                    'Sub-Category':secCatName,
                    'Image':all_img_links[i],
                    'Trending':trendingInfo[i],
                    'Brand':companyName[i],
                    'Product-info':moreProductInfo[i]
                }
                print(fin)
                allProducts.append(fin)
    
    driver.quit()
    return allProducts
        


# In[7]:


getAllProducts(driver)


# In[8]:


print(len(allProducts))
client = MongoClient('mongodb+srv://user:'+urllib.parse.quote('Avik@838')+'@cluster0.pe7lw.mongodb.net/intelFashion?retryWrites=true&w=majority')
print(client)
db = client['intelFashion']
flipkartProducts = db.flipkart
print(flipkartProducts)
flipkartProducts.remove()
# result = myntraProducts.insert_many(allProducts)
result = flipkartProducts.insert_many([{'i': i,'Major-Category':allProducts[i]['Major-Category'],'Sub-Category':allProducts[i]['Sub-Category'],'Image':allProducts[i]['Image'],'Trending':allProducts[i]['Trending'],'Brand':allProducts[i]['Brand'],'Product-Info':allProducts[i]['Product-info']} for i in range(len(allProducts))]).inserted_ids
print(result)


# In[ ]:




