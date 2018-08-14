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

__version__ = "1.0.0"


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


	def getReadFileUrl(self):

		# Read File
		for u in self.readFile():
			try:
				urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
				r = requests.get(u, verify=False, timeout=5).text	
				soup = BeautifulSoup(r, "html.parser")
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
			urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
			r = requests.get(url, verify=False, timeout=5).text
			soup = BeautifulSoup(r, "html.parser")
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
		text = requests.get('http://www.iana.org/domains/root/db').text
		soup = BeautifulSoup(text, "html.parser")
		link = soup.find('table', {'id': 'tld-table'})
		tlds = [anchor.text for anchor in link.find_all('a')]
		return tlds


	def getSource(self):

		self.getReadFileUrl()

		jobs = []
		links = []
		p = pool.Pool(20)
		
					
		#Get RootDomains		
		for allRootDomains in self.getRootDomains():
			https = "https://www."+self.org+allRootDomains
			http = "http://www."+self.org+allRootDomains
			#Check http(s) urls 
			l = [https,http]
			for url in l:
				jobs.append(p.spawn(self.getUrl, url))
		gevent.joinall(jobs)


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
		for tl in trademarkList:
			noUnicode = tl.encode('ascii', 'ignore')
			print(noUnicode)	
			text = input(" yes/no(press enter)  ")
			if text == "yes":
				trademarkList2.append(tl)
				directory = "results/"+self.org+"/"
				line = tl.rstrip('\n') 
				if(len(line) < 40): 
					self.write(directory,"unique_trademarks.txt",tl)

			else:
				continue	

		#Trademark test is starting		
		for trademarkList3 in trademarkList2:
			utf8EncodedTrademarks = trademarkList3.encode('utf-8')
			print("Trademark test is starting")
			#Check Google
			self.getGoogle(trademarkList3)				
 

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
		search.submit();
		con = input("Recaptcha? OK ")		
		if con == "ok":
			pass
		print("Go Go Go!")		
		try:
			i=2		
			while i < 11:   
				links = driver.find_elements_by_css_selector('div > h3.r > a')					
				urlList = []	
				for url in links:	
					print(url.get_attribute("href"))
					urlList.append(url.get_attribute("href"))
					for urls in urlList:
						print(urls)
						directory = "results/"+self.org+"/"
						self.write(directory,"google.txt",urls)
						

				map = driver.find_element_by_xpath("//a[@aria-label='Page "+str(i)+"']")
				
				i += 1
				time.sleep(randint(5,15))	
				map.click()

		except NoSuchElementException as e:
			print("No Such Element")
			pass
			#print(str(e))	
			#driver.quit()			

		
		driver.quit()	

class ParseDomain:

	def __init__(self,organization):
		self.org = organization


	def getGoogleDomains(self):

		googleList = []
		file = "results/"+self.org+"/google.txt"
		fh = open(file)
		for line in fh:	
			extracted = tldextract.extract(line)
			tld = extracted.domain+"."+extracted.suffix
			if tld not in googleList:
				googleList.append(tld)
		for domain in googleList:
			print(domain)
		fh.close() 

	def getTrademarks(self):

		file = "results/"+self.org+"/unique_trademarks.txt"
		fh = open(file)
		for line in fh:	
			print(line)
		fh.close() 



print('%s' % (white))
parser = argparse.ArgumentParser(description='Köstebek') 
parser.add_argument('-u', help='Url List') 
parser.add_argument('-n', help='Organization Name') 
parser.add_argument('-g', help='Google Domains') 
parser.add_argument('-t', help='Company Trademarks') 
args = parser.parse_args()

if len(sys.argv) == 1:
	parser.print_help()
	print("\n Example Usage :\n\n Trademark Scan :  python3 kostebek.py -u list.txt -n Organization Name \n Get Google Domains  : python3 kostebek.py -g Organization Name \n Get Company Trademarks : python3 kostebek.py -t Organization Name\n ")
	sys.exit()

if args.g is not None:
	core = ParseDomain(args.g)
	core.getGoogleDomains()
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

