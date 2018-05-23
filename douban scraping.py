# -*- coding: utf-8 -*-
"""
Created on Thu May 10 01:38:55 2018

@author: lhs
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May  9 16:31:09 2018

@author: lhs
"""

import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
import re
import pandas as pd
import json
global doubantop250
doubantop250=pd.DataFrame(columns=['Title','Director','Year','Country','Type','Rating'])
def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None
def parse_one_page(html):
    pattern=re.compile('<li>.*?<em class="">(.*?)</em>.*?<span class="title">(.*?)</span>.*?<p class="">(.*?)&nbsp.*?<br>(.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?average">(.*?)</span>.*?',re.S)
    items=re.findall(pattern,html)
    return items
    

        
def main(start):
    url='https://movie.douban.com/top250?start='+str(start)+'&filter='
    html=get_one_page(url)
    items=parse_one_page(html)
    for item in items:
       doubantop250.loc[item[0]]=[item[1],item[2].strip()[4:],item[3].strip(),item[4],item[5].strip(),item[6]]

if __name__ =='__main__':
    for i in range(10):
        main(i*25)
    doubantop250.to_csv('doubantop250.csv',encoding='utf_8_sig',sep=",")
   #pool=Pool()
   #pool.map(main,[i*25 for i in range(10)])

