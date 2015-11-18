"""
This script use selenium web driver to scrap website which uses ajax to fetch data
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib2
from subprocess import call
from datetime import date
import redis
import requests
import base64
import random
import tinys3
import time
import MySQLdb
import hashlib
import sys
from os import listdir
from os.path import isfile, join
import json
from requests.auth import HTTPProxyAuth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re

class Sel(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        self.base_url = "url"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        i=1
        driver = self.driver
        delay = 3
        driver.get(self.base_url) #+ "/search?q=stckoverflow&src=typd")
        driver.find_elements_by_xpath("//div[@id='newLoading']")
        print " i m in div"
        #driver.find_element_by_id('newLoading').click()
        while i<11:
            print i
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            """
            html_source = driver.page_source
            data = html_source.encode('utf-8')
            #print data
            elem = driver.find_elements_by_id('linkToDetails')
            for link in elem:
                yup= link.get_attribute('href')
                print yup
                with open("carwale.txt",'a') as gh:
                    gh.write(yup+"\n")   
            """
            time.sleep(8)
            if(i>5):
                #driver.find_element_by_partial_link_text('Show More Cars').click()
                print "button clicked"
                driver.find_element_by_xpath("//*[@id='Form1']/section[2]/div[1]/div[4]/div[3]/a").click()
                print " i m in button"
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                html_source = driver.page_source
                data = html_source.encode('utf-8')
                #print data
                if(i==10):
                    elem = driver.find_elements_by_id('linkToDetails')
                    for link in elem:
                        yup1= link.get_attribute('href')
                        print yup1
                        with open("delhi_carwale.txt",'a') as gh:
                            gh.write(yup1+"\n")     
                    
                time.sleep(10)
                print driver.find_element_by_xpath("//*[@id='Form1']/section[2]/div[1]/div[4]/div[3]/a").text
                print "i m out button"      
            i+=1
            

if __name__ == "__main__":
    unittest.main()
