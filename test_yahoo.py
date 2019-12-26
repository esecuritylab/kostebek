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

def getYahoo(dork):

	chrome_options = Options()
	chrome_options.add_argument("--window-size=1920x1080")
	chrome_options.add_argument("--disable-infobars")
	chrome_options.add_argument("--disable-dev-shm-usage") 
	chrome_options.add_argument("disable-infobars")
	chrome_options.add_argument("--no-sandbox") 
	chrome_driver = "/usr/local/bin/chromedriver"

	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	driver.get('https://www.yahoo.com')
	driver.implicitly_wait(20)

	
	# bypass = driver.find_element_by_xpath("/html/body/div/div/div/form/div/button[2]")
	# bypass.click()
	# time.sleep(2)

	search = driver.find_element_by_name('p')	
	dork2 = 'intext:"'+dork+'"'
	time.sleep(3)
	search.send_keys(dork2)
	search.submit();
	try:
		i=1
		while i < 11:

			time.sleep(3) 
			links = driver.find_elements_by_css_selector('div.dd.algo.algo-sr.Sr > div > h3 > a')	
			for url in links:
				print(url.get_attribute("href"))

			time.sleep(5)
			map = driver.find_element_by_xpath("//*[contains(@title, '"+str(i)+"1')]")

			map.click()
			time.sleep(2)
			i += 1

	except NoSuchElementException as e:
		print("No Such Element")
		
		driver.quit()	

getYahoo("© Company 2019")	
