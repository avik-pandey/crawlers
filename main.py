#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os                                                                       
from multiprocessing import Pool 
import defs


# In[2]:


processes = ('myntra.py', 'vogue_crawler.py','flipkart.py') 
# def run_process(process):                                                             
#     os.system('python {}'.format(process)) 

    


# In[3]:


pool = Pool(processes=3)                                                        
pool.map(defs.run_process, processes) 


# In[ ]:




