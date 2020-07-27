#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os                                                                       
from multiprocessing import Pool 
import defs


# In[5]:


processes = ('myntra.py', 'vogue_crawler.py','flipkart.py') 
# def run_process(process):                                                             
#     os.system('python {}'.format(process)) 

    


# In[ ]:


if __name__ == '__main__':    
    pool = Pool(processes=3)                                                        
    pool.map(defs.run_process, processes) 


# In[ ]:




