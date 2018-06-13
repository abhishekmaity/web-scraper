# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:42:47 2018

@author: Abhishek

Python class to scrap link of every restaurant whose zomato page link 
is given on https://www.zomato.com/bangalore/restaurants

I am using BeautifulSoup for parsing HTML, Gecko driver in Selenium for Firefox 
browser to make requests instead of scripts to Zomato.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import sys

browser = None

try:
    browser = webdriver.Firefox()
except Exception as error:
    print(error)
#for handling any error while requesting via firefox

out_file = open("restaurant_details.txt", "ab")
# "ab" - Opens a file for appending in binary format

class ZomatoRestaurantLinkGrab:
    '''
    The class is used to define the procedure of accessing the browser for 
    grabbing the URLs of restaurants present in the Zomato webpage(s)
    '''
    def __init__(self, url):
        self.url = url
        self.html_text = None
        try:
            browser.get(self.url)
            self.html_text = browser.page_source
            
        except Exception as err:
            print(str(err))
            return
        else:
            print('Access successful.')

        self.soup = None
        if self.html_text is not None:
            self.soup = BeautifulSoup(self.html_text, 'lxml')

    def scrap(self):
        '''
        The method defined here grabs the individual restaurant URL on a page 
        using the unique <a> tag having attributes unique to every restaurant 
        and assimilate together in the file.
        '''
        soup = self.soup
        for tag in soup.find_all("a", attrs={'data-result-type': 'ResCard_Name'}):
            out_file.write(tag['href'].encode('utf-8').strip() + b'\n')


if __name__ == '__main__':
    if browser is None:
        print("Selenium not opened")
        sys.exit()

    for x in range(1, 4):
        #currently there are total 592 pages for list of restaurants in 
        #bangalore zomato website. For this assignment I have only assumed to 
        #navigate only 3 pages.
        
        #for loop to navigate all the pages containing the restaurants
        print(str(x) + '\n')
        #To display the page that is being accessed currently
        zr = ZomatoRestaurantLinkGrab('https://www.zomato.com/bangalore/restaurants?page={}'.format(x))
        zr.scrap()
        
    browser.close()
    out_file.close()
