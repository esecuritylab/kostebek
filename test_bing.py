import gevent
from gevent import monkey, pool
monkey.patch_all()
from gevent import ssl
import os, sys, time
import requests
from bs4 import BeautifulSoup
import urllib3
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from random import randint
import argparse 
import tldextract 

def getBing(dork):

	chrome_options = Options()
	chrome_options.add_argument("--window-size=1920x1080")
	chrome_options.add_argument("--disable-infobars")
	chrome_options.add_argument("--disable-dev-shm-usage") 
	chrome_options.add_argument("disable-infobars")
	chrome_options.add_argument("--no-sandbox") 
	chrome_driver = "/usr/local/bin/chromedriver"

	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	driver.get('https://www.bing.com')
	driver.implicitly_wait(10)
	search = driver.find_element_by_name('q')	
	dork2 = 'intext:"'+dork+'"'
	time.sleep(3)
	search.send_keys(dork2)
	search.submit();
	try:
		i=3
		while i < 11: 
			links = driver.find_elements_by_css_selector('.b_algo h2 a')	
			for url in links:
				print(url.get_attribute("href"))
			time.sleep(3)
			count = len(driver.find_elements_by_xpath("//*[@id=\"b_results\"]/li"))	
			print(count)	
			map = driver.find_element_by_xpath("//*[@id=\"b_results\"]/li["+str(count)+"]/nav/ul/li["+str(i)+"]/a")
			i += 1
			print("simdi tikla"+str(i))	
			map.click()

		#driver.quit()	

	except NoSuchElementException as e:
		print("No Such Element")
		pass
		#print(str(e))	
		#driver.quit()			

getBing(" © Company 2019 ")	

