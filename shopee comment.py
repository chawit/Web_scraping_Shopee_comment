# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:02:54 2018

@author: lhs
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
from selenium.common.exceptions import TimeoutException
import pandas as pd
from math import ceil

url='https://shopee.sg/%F0%9F%93%B2FreeNinjaVan-Mail%F0%9F%94%A5-A-JAYS-FIVE-WINDOW-EARPHONE-earpiece-A-JAYS-FIVE-a-jays-5-i.34664819.484690888'

shopee=webdriver.Chrome()
wait=WebDriverWait(shopee, 10)
def search2():
    try:
        shopee.get(url)
        shopee.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ratings=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                       '#main > div > div.shopee-page-wrapper > div:nth-child(2) > div.product-page > div > div:nth-child(4) > div > div > ul > li:nth-child(2)')))
        ratings.click()
        with_comment=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                            '#main > div > div.shopee-page-wrapper > div:nth-child(2) > div.product-page > div > div:nth-child(4) > div > div > div > div > div.shopee-product-rating-overview > div.shopee-product-rating-overview__section-2 > div.shopee-product-rating-overview__filter.shopee-product-rating-overview__filter--with-comment')))
        comment_cnt=int(re.compile('(\d+)').search(with_comment.text).group(1))
        with_comment.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   '#main > div > div.shopee-page-wrapper > div:nth-child(2) > div.product-page > div > div:nth-child(4) > div > div > div > div > div.shopee-product-rating-overview > div.shopee-product-rating-overview__section-2 > div.shopee-product-rating-overview__filter.shopee-product-rating-overview__filter--active.shopee-product-rating-overview__filter--with-comment')))
        return comment_cnt
    except TimeoutException:
        return search2()
    
def get_comments():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#main > div > div.shopee-page-wrapper > div:nth-child(2) > div.product-page > div > div:nth-child(4) > div > div > div > div > div:nth-child(2) > div.shopee-product-comment-list .shopee-product-rating ')))
    html=shopee.page_source
    doc=pq(html)
    items=doc('.shopee-product-comment-list .shopee-product-rating .shopee-product-rating__main').items()
    #items=shopee.find_elements_by_css_selector('#main > div > div.shopee-page-wrapper > div:nth-child(2) > div.product-page > div > div:nth-child(4) > div > div > div > div > div:nth-child(2) > div.shopee-product-comment-list .shopee-product-rating')
    for item in items:
        comment.append([item.find('.shopee-product-rating__author-name').text(),
                        item.find('.shopee-product-rating__content').text(),
                        item.find('.shopee-product-rating__time').text()]
                        )
    
def next_page():
    nextpage=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           '#main > div > div.shopee-page-wrapper > div:nth-child(2) > div.product-page > div > div:nth-child(4) > div > div > div > div > div:nth-child(2) > div.shopee-page-controller > button.shopee-icon-button.shopee-icon-button--right')))
    nextpage.click()
    get_comments()
    
def main():
    comment_cnt=search2()
    page_num=ceil(comment_cnt/10)
    get_comments()
    for i in range(2,page_num+1):
        next_page()

if __name__=='__main__':
    global comment
    comment=[]
    main()