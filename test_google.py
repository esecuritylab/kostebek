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

def getGoogle(dork):

	chrome_options = Options()
	chrome_options.add_argument("--window-size=1920x1080")
	chrome_options.add_argument("--disable-infobars")
	chrome_options.add_argument("--disable-dev-shm-usage") 
	chrome_options.add_argument("disable-infobars")
	chrome_options.add_argument("--no-sandbox") 
	chrome_driver = "/usr/local/bin/chromedriver"

	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	driver.get('http://www.google.com')
	driver.implicitly_wait(20)
	search = driver.find_element_by_name('q')
	dork2 = 'intext:"'+dork+'"'
	search.send_keys(dork2)
	search.submit()
	driver.implicitly_wait(20)
	src = driver.page_source
	if 'Our systems have detected unusual traffic from your computer network' in src:
		con = input("Recaptcha? OK ")		
		if con == "ok":
			pass
			print("Go Go Go!")
	else:
		print("STOP")

		
	try:
		i=2		
		while i < 11:   
			links = driver.find_elements_by_css_selector('.r > a')	
			print(links)				
			urlList = []	
			for url in links:	
				print(url.get_attribute("href"))
				urlList.append(url.get_attribute("href"))
				for urls in urlList:
					print(urls)
					
						

			map = driver.find_element_by_xpath("//a[@aria-label='Page "+str(i)+"']")
			
			i += 1
			map.click()

	except NoSuchElementException as e:
		print("No Such Element")
		pass
		#print(str(e))	
		#driver.quit()			

		
		driver.quit()	

getGoogle("© Company 2019")		
