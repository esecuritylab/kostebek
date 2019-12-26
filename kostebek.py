#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Colors
white = '\033[97m'
green = '\033[92m'
red = '\033[91m'
yellow = '\033[93m'
end = '\033[0m'
back = '\033[7;91m'
info = '\033[93m[!]\033[0m'
que = '\033[94m[?]\033[0m'
bad = '\033[91m[-]\033[0m'
good = '\033[32m[+]\033[0m'
run = '\033[97m[~]\033[0m'

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





logo = """
  _  __  _   _         _            _              _    
 | |/ / (_) (_)       | |          | |            | |   
 | ' /    ___    ___  | |_    ___  | |__     ___  | | __
 |  <    / _ \  / __| | __|  / _ \ | '_ \   / _ \ | |/ /
 | . \  | (_) | \__ \ | |_  |  __/ | |_) | |  __/ |   < 
 |_|\_\  \___/  |___/  \__|  \___| |_.__/   \___| |_|\_\
														
""" 

__version__ = "1.1.0"


def banner():
	print("""%s
 Köstebek Reconnaissance tool 
 Author: Evren (@evrnyalcin)
 Contributors: Burak (@A_Burak_Gokalp)
 https://www.github.com/esecuritylab/kostebek
 Version: %s
""" % (red, __version__ ))

print('%s%s' % (red, logo))

banner()

class kostebek:

	def __init__(self,filename,organization):
		self.filename = filename
		self.org = organization
		self.bank = {}
		self.log = []

	def readFile(self):
		try:
			data = [line.strip() for line in open(self.filename, 'r')]
			return data
		except IOError as error:
			print(error)
			sys.exit(0)

	def write(self,directory,filename,string):

		if not os.path.exists(directory):
			os.makedirs(directory)
			
		d = "results/"+self.org+"/"+filename
		with open(d, 'a'):
			os.utime(d, None)
		with open(d, "a") as f:
			f.write(string+'\n')

	def soup(self, url):
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		r = requests.get(url, verify=False, timeout=2).text	
		soup = BeautifulSoup(r, "html.parser")
		return soup				


	def getReadFileUrl(self):

		# Read File
		for u in self.readFile():
			try:
				soup = self.soup(u)
				for copyrightAll in ["©","®"]:
					pattern = re.compile(str(copyrightAll))
					getTrademarks = soup.find(text=pattern)
					if getTrademarks is not None:
						if copyrightAll in getTrademarks:
							if(len(getTrademarks) < 40): 
								noUnicode = getTrademarks.encode('ascii', 'ignore')			
								print('%s URL: %s String: %s Match: %s ' % (good, u, copyrightAll, noUnicode))
								merge = self.org+u
								self.bank.setdefault(merge, []).append(getTrademarks)
							

			except requests.exceptions.Timeout as ert:
				print("Connection Timeout")
				#self.log.append(ert)
			except requests.exceptions.TooManyRedirects as errt:
				print ("Too Many Redirects Error")
				#self.log.append(errt)
			except requests.exceptions.RequestException as errr:
				print("Connection Error")
				#self.log.append(errr)


	def getUrl(self,url):
		try:
			soup = self.soup(url)
			copyright1 = "©"
			copyright2 = "®"
			for copyrightAll in copyright1,copyright2:
				pattern = re.compile(str(copyrightAll))
				getTrademarks = soup.find(text=pattern)
				if getTrademarks is not None:
					if copyrightAll in getTrademarks:
						if(len(getTrademarks) < 40):
							noUnicode = getTrademarks.encode('ascii', 'ignore')
							print('%s URL: %s String: %s Match: %s ' % (good, url, copyrightAll, noUnicode ))
							self.bank.setdefault(url, []).append(getTrademarks)

		except requests.exceptions.Timeout as ert:
			print("Connection Timeout: "+url)
			#self.log.append(ert)
		except requests.exceptions.TooManyRedirects as errt:
			print ("Too Many Redirects Error:",errt)
			#self.log.append(errt)
		except requests.exceptions.RequestException as errr:
			print("Connection Error: "+url)
			#self.log.append(errr)
	


	def getRootDomains(self):

		url = "http://www.iana.org/domains/root/db"
		soup = self.soup(url)
		link = soup.find('table', {'id': 'tld-table'})
		tlds = [anchor.text for anchor in link.find_all('a')]
		
		#Get RootDomains
		
		jobs = []
		links = []
		p = pool.Pool(20)

		for allRootDomains in tlds:
			https = "https://www."+self.org+allRootDomains
			http = "http://www."+self.org+allRootDomains
			#Check http(s) urls 
			l = [https,http]
			for url in l:
				jobs.append(p.spawn(self.getUrl, url))
		gevent.joinall(jobs)		


	def getSource(self):

		self.getReadFileUrl()
					
		self.getRootDomains()


		#Write AllTrademarks			
		trademarkList = []	
		for i in self.bank.values():
			for p in i:
				if p not in trademarkList:
					trademarkList.append(p)
					directory = "results/"+self.org+"/"
					line = p.rstrip('\n') 
					if(len(line) < 40):
						self.write(directory,"all_trademarks.txt",p)

		#Write Unique Trademarks					
		trademarkList2 = []	
		trademarkList_bing = []	
		trademarkList_yahoo = []			
		for tl in trademarkList:
			noUnicode = tl.encode('ascii', 'ignore')
			print(noUnicode)	
			text = input(" yes/no(press enter)  ")
			if text == "yes":
				trademarkList2.append(tl)
				trademarkList_bing.append(tl)
				trademarkList_yahoo.append(tl)
				directory = "results/"+self.org+"/"
				line = tl.rstrip('\n') 
				if(len(line) < 40): 
					self.write(directory,"unique_trademarks.txt",tl)

			else:
				continue	

		#google Trademark test is starting		
		for trademarkList3 in trademarkList2:
			utf8EncodedTrademarks = trademarkList3.encode('utf-8')
			print("Google Trademark test is starting")
			#Check Google
			self.getGoogle(trademarkList3)	

		#Bing Trademark test is starting	
		for trademarkList4 in trademarkList_bing:
			utf8EncodedTrademarks = trademarkList4.encode('utf-8')
			print("Bing Trademark test is starting")
			#Check Bing
			self.getBing(trademarkList4)	

		#Yahoo Trademark test is starting	
		for trademarkList5 in trademarkList_yahoo:
			utf8EncodedTrademarks = trademarkList5.encode('utf-8')
			print("Yahoo Trademark test is starting")
			#Check Bing
			self.getYahoo(trademarkList5)	

				


	def getGoogle(self,dork):

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
		time.sleep(randint(2,5))
		search.send_keys(dork2)
		search.submit()

		driver.implicitly_wait(20)
		src = driver.page_source
		if 'Our systems have detected unusual traffic from your computer network' in src:
			con = input("Recaptcha? OK ")		
			if con == "ok":
				pass
		else:
			print("STOP")

		try:
			i=2	
			while i < 11:   
				links = driver.find_elements_by_css_selector('.r > a')	
				#print(links)				
				urlList = []	
				for url in links:	
					#print(url.get_attribute("href"))
					urlList.append(url.get_attribute("href"))
				for urls in urlList:
					print(urls)
					directory = "results/"+self.org+"/"
					self.write(directory,"google.txt",urls)
						

				map = driver.find_element_by_xpath("//a[@aria-label='Page "+str(i)+"']")
				
				i += 1
				time.sleep(1)	
				map.click()

		except NoSuchElementException as e:
			print("No Such Element")	
			driver.quit()			

		
		driver.quit()	

	def getBing(self, dork):

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
			# i=3
			# while i < 11: 
			# 	links = driver.find_elements_by_css_selector('.b_algo h2 a')	
			# 	urlList = []	
			# 	for url in links:
			# 		print(url.get_attribute("href"))
			# 		urlList.append(url.get_attribute("href"))
			# 		for urls in urlList:
			# 			print(urls)
			# 			directory = "results/"+self.org+"/"
			# 			self.write(directory,"bing.txt",urls)

			# 	time.sleep(3)
			# 	count = len(driver.find_elements_by_xpath("//*[@id=\"b_results\"]/li"))	
			# 	print(count)	
			# 	map = driver.find_element_by_xpath("//*[@id=\"b_results\"]/li["+str(count)+"]/nav/ul/li["+str(i)+"]/a")
			# 	i += 1	
			# 	map.click()	
			i=3
			while i < 11: 
				links = driver.find_elements_by_css_selector('.b_algo h2 a')
				urlList = []	
				for url in links:
					print(url.get_attribute("href"))
					urlList.append(url.get_attribute("href"))
				for urls in urlList:
					#print(urls)
					directory = "results/"+self.org+"/"
					self.write(directory,"bing.txt",urls)

				time.sleep(3)
				count = len(driver.find_elements_by_xpath("//*[@id=\"b_results\"]/li"))	
				print(count)	
				map = driver.find_element_by_xpath("//*[@id=\"b_results\"]/li["+str(count)+"]/nav/ul/li["+str(i)+"]/a")
				i += 1
				print("simdi tikla"+str(i))	
				map.click()


		except NoSuchElementException as e:
			print("No Such Element")
			driver.quit()

		driver.quit()	

	def getYahoo(self, dork):

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
				urlList = []	
				for url in links:
					print(url.get_attribute("href"))
					urlList.append(url.get_attribute("href"))
				for urls in urlList:
					print(urls)
					directory = "results/"+self.org+"/"
					self.write(directory,"yahoo.txt",urls)

				time.sleep(5)
				map = driver.find_element_by_xpath("//*[contains(@title, '"+str(i)+"1')]")

				map.click()
				time.sleep(2)
				i += 1

		except NoSuchElementException as e:
			print("No Such Element")
			driver.quit()	

		driver.quit()	


class ParseDomain:

	def __init__(self,organization):
		self.org = organization


	def getGoogleDomains(self):

		googleList = []
		file = "results/"+self.org+"/google.txt"
		if os.path.exists(file):
			fh = open(file)
			for line in fh:	
				extracted = tldextract.extract(line)
				tld = extracted.domain+"."+extracted.suffix
				if tld not in googleList:
					googleList.append(tld)
			for domain in googleList:
				print(domain)
			fh.close() 
		else:
			print("Not found")
			exit()	


	def getBingDomains(self):

		googleList = []
		file = "results/"+self.org+"/bing.txt"
		if os.path.exists(file):
			fh = open(file)
			for line in fh:	
				extracted = tldextract.extract(line)
				tld = extracted.domain+"."+extracted.suffix
				if tld not in googleList:
					googleList.append(tld)
			for domain in googleList:
				print(domain)
			fh.close()
		else:
			print("Not found")
			exit()	
				 

	def getYahooDomains(self):

		googleList = []
		file = "results/"+self.org+"/yahoo.txt"
		if os.path.exists(file):
			fh = open(file)
			for line in fh:	
				extracted = tldextract.extract(line)
				tld = extracted.domain+"."+extracted.suffix
				if tld not in googleList:
					googleList.append(tld)
			for domain in googleList:
				print(domain)
			fh.close()
		else:
			print("Not found")
			exit()	


	def getTrademarks(self):

		file = "results/"+self.org+"/unique_trademarks.txt"
		if os.path.exists(file):
			fh = open(file)
			for line in fh:	
				print(line)
			fh.close() 
		else:
			print("Not found")
			exit()	



print('%s' % (white))
parser = argparse.ArgumentParser(description='Köstebek') 
parser.add_argument('-u', help='Url List') 
parser.add_argument('-n', help='Organization Name') 
parser.add_argument('-g', help='Google Domains') 
parser.add_argument('-b', help='Bing Domains') 
parser.add_argument('-y', help='Yahoo Domains')
parser.add_argument('-t', help='Company Trademarks') 
args = parser.parse_args()

if len(sys.argv) == 1:
	parser.print_help()
	print("\n Example Usage :\n\n Trademark Scan :  python3 kostebek.py -u list.txt -n Organization Name \n Get Google Domains  : python3 kostebek.py -g Organization Name \n Get Bing Domains  : python3 kostebek.py -b Organization Name \n Get Yahoo Domains  : python3 kostebek.py -y Organization Name  \n Get Company Trademarks : python3 kostebek.py -t Organization Name\n ")
	sys.exit()

if args.g is not None:
	core = ParseDomain(args.g)
	core.getGoogleDomains()
	sys.exit()

if args.b is not None:
	core = ParseDomain(args.b)
	core.getBingDomains()
	sys.exit()	

if args.y is not None:
	core = ParseDomain(args.y)
	core.getYahooDomains()
	sys.exit()	

if args.t is not None:
	core = ParseDomain(args.t)
	core.getTrademarks()
	sys.exit()	

core = kostebek(args.u,args.n)

try:	
	core.getSource()
except KeyboardInterrupt:
	print('Interrupted')
	sys.exit(0)		



