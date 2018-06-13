# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 18:44:54 2018

@author: Abhishek

Python class to scrap data for a particular restaurant whose zomato link 
is obtained via restaurant_list.py program

I am using BeautifulSoup for parsing HTML, Gecko driver in Selenium for Firefox 
browser to make requests instead of scripts to Zomato.
"""

import re
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request
from selenium import webdriver
from bs4 import NavigableString
import sys
import json

browser = None
try:
    browser = webdriver.Firefox()
except Exception as error:
    print(error)
#for handling any error while requesting via firefox 

class ZomatoRestaurant:
    '''
    The class is used to define the procedure of accessing and grabbing all the
    details like name, rating, address, type of cuisines served, lat-long etc from 
    the restaurant pages stored in 'restaurant_details.txt'.   
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
        The method defined here grabs the details of restaurant from their
        respective URLs on the page using the unique HTML tag(s) having attributes 
        containing the required data and assimilate together in the output JSON file.
        '''
        if self.soup is None:
            return {}
        soup = self.soup
        rest_details = dict()
        #varaiable to store the data obtained in a dictionary

        name_anchor = soup.find("a", attrs={"class": "ui large header left"})
        if name_anchor:
            rest_details['name'] = name_anchor.text.strip()
        else:
            rest_details['name'] = ''
        #This captures the NAME of the restaurant

        rating_div = soup.find("div", attrs={"class": re.compile("rating-for")})
        if rating_div:
            rest_details['rating'] = rating_div.text.strip()[:-2]
        else:
            rest_details['rating'] = 'N'  # default on non-availability of rating
        #This captures the average RATINGS given to the restaurant

        contact_span = soup.find("span", attrs={"class": 'tel'})
        if contact_span:
            rest_details['contact'] = contact_span.text.strip()
        else:
            rest_details['contact'] = ''
        #This captures the CONTACT details(phone no or/and mobile no) of the restaurant

        cuisine_box = soup.find('div', attrs={'class': 'res-info-cuisines clearfix'})
        rest_details['cuisines'] = []
        if cuisine_box:
            for it in cuisine_box.find_all('a', attrs={'class': 'zred'}):
                rest_details['cuisines'].append(it.text)
        #This captures the variety of CUISINES served at the restaurant

        geo_locale = soup.find("div", attrs={"class": "resmap-img"})
        if geo_locale:
            geo_url = geo_locale.attrs['data-url']
            parsed_url = urlparse(geo_url)
            geo_arr = str(urllib.parse.parse_qs(parsed_url.query)['center']).split(',')
            rest_details['geo_location'] = [re.sub("[^0-9\.]", "", geo_arr[0]), re.sub("[^0-9\.]", "", geo_arr[1])]
        if 'geo_location' not in rest_details:
            rest_details['geo_location'] = ['undefined', 'undefined']
        ##This captures the lat-long CO-ORDINATES using the regex from HTML parsed of the restaurant

        address_div = soup.find("div", attrs={"class": "resinfo-icon"})
        if address_div:
            rest_details['address'] = address_div.span.get_text()
        else:
            rest_details['address'] = ""
        #This captures the ADDRESS of the restaurant

        rest_details['what_people_love_here'] = []
        for div in soup.find_all("div", attrs={'class': 'rv_highlights__section pr10'}):
            child_div = div.find("div", attrs={'class': 'grey-text'})
            if child_div:
                rest_details['what_people_love_here'].append(child_div.get_text())
        return rest_details
        #This captures the avg. REVEIWS of the restaurant


if __name__ == '__main__':
    if browser is None:
        sys.exit()
    out_file = open("zomato_bangalore.json", "a")
    with open('restaurant_details.txt', 'r', encoding="utf-8") as f:
        for line in f:
            zr = ZomatoRestaurant(line)
            json.dump(zr.scrap(), out_file)
            out_file.write('\n')
    out_file.close()
    browser.close()
    