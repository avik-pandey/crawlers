#!/usr/bin/env python
# coding: utf-8

# In[8]:


import selenium
from selenium.webdriver import ActionChains


# In[9]:


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
myntraProducts = db.myntra
print(myntraProducts)


# In[10]:


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


# In[11]:


allCategories = []
def getCategories(driver,base_url = "https://www.myntra.com/"):
    try:
        
        driver = patching_get(driver,base_url)
        menPath = driver.find_element_by_xpath('//*[@id="desktop-header-cnt"]/div[2]/nav/div/div[1]/div/a')
        womenPath = driver.find_element_by_xpath('//*[@id="desktop-header-cnt"]/div[2]/nav/div/div[2]/div/a')
        kidsPath = driver.find_element_by_xpath('//*[@id="desktop-header-cnt"]/div[2]/nav/div/div[3]/div/a')
#     paths = []
#     paths.append(menPath)
#     paths.append(womenPath)
#     paths.append(kidsPath)
#     fake = 0
#     for el in paths:
#         hover = ActionChains(driver).move_to_element(el)
#         hover.perform()
#         time.sleep(10)
#         primaryCat = el.text
#         print(primaryCat)
#         categories = driver.find_elements_by_class_name('desktop-categoryName')
# #         print(categories)
#         catArr = []
#         print(len(categories))
#         for cat in categories:
#             catLink = driver.find_elements_by_class_name('desktop-categoryLink')
#             #catLinkText = driver.find_elements_by_class_name('desktop-categoryLink')
#             catName = cat.text
# #             print(catName)
            
#             links = []
#             for link in catLink:
# #                 print(link.text)
#                 linkHref = link.get_attribute('href')
#                 linkName = link.text
                
#                 finLink = []
#                 finLink.append(linkHref)
#                 finLink.append(linkName)
# #                 finLink.append(primaryCat)
#                 links.append(finLink)
            
#             catArr.append(catName)
#             catArr.append(links)
#         allCategories.append(catArr)
        majCategories = driver.find_elements_by_class_name('desktop-categoryContainer')
        print(len(majCategories))
        cnt = 0
        for el in majCategories:
            cnt = cnt+1
            if(cnt>2):
                break
            majCatName = ""
            if(cnt == 1):
                majCatName = menPath.text
            elif(cnt == 2):
                majCatName = womenPath.text
            else:
                majCatName = kidsPath.text
            lowCategories = el.find_elements_by_tag_name('a')
            tot = []
            allLinks = []
            for lowCat in lowCategories:
                singleLink = []
                name = lowCat.get_attribute('textContent')
            
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
        
    


# In[12]:


getCategories(driver)


# In[13]:


allProducts = []

def getAllProducts(driver):
    try:
        
        for el in allCategories:
            majCatName = el[0]
            print(majCatName)
            for e in el[1]:
                secCatName = e[0]
                print(secCatName)
                driver = patching_get(driver,e[1])
                try:
                
                    img_links = driver.find_elements_by_class_name('product-sliderContainer')
                    time.sleep(3)
                except:
                    pass
                print(len(img_links))
                myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.TAG_NAME,"img"))))
#             images = driver.find_elements_by_tag_name('img')
                images = []
                while True:
            
                    driver.execute_script("window.scrollBy(0,800)", "")
                    try:
                        WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_tag_name("img")) > myLength)
                        images = driver.find_elements_by_tag_name("img")
                        myLength = len(images)
                    except TimeoutException:
                        break
                print(len(images))
                all_img_links = []
                for ele in images:
                    imgLink = ele.get_attribute('src')
                    time.sleep(0.1)
                    imgLink = ele.get_attribute('src')
                    all_img_links.append(imgLink)
                
                print(len(all_img_links))
            
                trendingInfo = []
                for image in img_links:
                #imgLink = image.find_element_by_class_name('img-responsive').get_attribute('src')
#                 try:
#                     imgLink = WebDriverWait(image, 20).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
#                 except TimeoutException:
#                     print('aacaa')
#                     pass
                    
                
#                 finImg = imgLink.get_attribute('src')
#                 print(finImg)
                    temp = False
                    try:
                        tmp1=image.find_element_by_class_name("xcelerator-plpXceleratorImageTag")
#                     time.sleep(0.1)
#                     tmp1 = image.find_element_by_class_name("xcelerator-plpXceleratorImageTag")
                        temp = True
                    except NoSuchElementException:
#                     print('amaa')
                         temp = False
                    
#                 all_img_links.append(finImg)
                    trendingInfo.append(temp)
             
                productInfo = driver.find_elements_by_class_name('product-productMetaInfo')
                companyName = []
                moreProductInfo = []
            
                for prod in productInfo:
                    brandName = prod.find_element_by_class_name('product-brand').text
                    productName = prod.find_element_by_class_name('product-product').text
                    companyName.append(brandName)
                    moreProductInfo.append(productName)
            
                size = len(companyName)
            
                for i in range(size):
                    if len(all_img_links) == 0:
                        break
                    fin = {
                    'majorCategory':majCatName,
                    'subCategory':secCatName,
                    'Image':all_img_links[i],
                    'Trending':trendingInfo[i],
                    'Brand':companyName[i],
                    'productInfo':moreProductInfo[i]
                   }
                    print(fin)
                    allProducts.append(fin)
    
    except Exception as e:
        print(e)
        raise(e)
    driver.quit()
    return allProducts
            
            
    


# In[14]:


getAllProducts(driver)


# In[15]:


print(len(allProducts))
client = MongoClient('mongodb+srv://user:'+urllib.parse.quote('flipkart')+'@cluster0.pe7lw.mongodb.net/intelFashion?retryWrites=true&w=majority')
print(client)
db = client['intelFashion']
myntraProducts = db.myntra
print(myntraProducts)
myntraProducts.remove()
# result = myntraProducts.insert_many(allProducts)
result = myntraProducts.insert_many([{'i': i,'majorCategory':allProducts[i]['majorCategory'],'subCategory':allProducts[i]['subCategory'],'Image':allProducts[i]['Image'],'Trending':allProducts[i]['Trending'],'Brand':allProducts[i]['Brand'],'productInfo':allProducts[i]['productInfo']} for i in range(len(allProducts))]).inserted_ids
print(result)
print(result)
# for object_id in result.inserted_ids:
#     print(str(object_id))


# In[ ]:





# In[ ]:




