# -*- coding: utf-8 -*-

# Import modules
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import requests
import pandas as pd
import re
import random
import time
import os.path
from os import path
import support as sp
from tqdm import tqdm
from random import randint
import datetime
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psutil
from selenium.common.exceptions import WebDriverException
import os


#Ignore SSL certificate errors
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


#Prepare txt file
timestamp=int(time.time())
filename = "booking_flag_url"+str(timestamp)+".txt"
filename2 = "booking_done_url"+str(timestamp)+".txt"
filename3= "booking_scraped_url"+str(timestamp)+".txt"
filename4="logs"+str(timestamp)+".txt"
# Modified version for France - these files are inactive
#filename5="booking_country_url"+str(timestamp)+".txt"
#filename5a="booking_country_url_list"+str(timestamp)+".txt"
#filename6="booking_city_url"+str(timestamp)+".txt"
#filename6a="booking_city_url_list"+str(timestamp)+".txt"
now = datetime.datetime.now()
fhandle = open(filename,"w", encoding="utf-8")
#Print timestamp file 1
print (now.strftime("%Y-%m-%d %H:%M:%S"),file=fhandle)
fhandle.close()
fhandle2 = open(filename2,"w", encoding="utf-8")
#Print timestamp file 2
print (now.strftime("%Y-%m-%d %H:%M:%S"),file=fhandle2)
fhandle2.close()
fhandle3 = open(filename3,"w", encoding="utf-8")
print (now.strftime("%Y-%m-%d %H:%M:%S"),file=fhandle3)
fhandle3.close()
fhandle4 = open(filename4,"w", encoding="utf-8")
print (now.strftime("%Y-%m-%d %H:%M:%S"),file=fhandle4)
fhandle4.close()
# Modified version for France - these files are inactive
#fhandle5 = open(filename5,"w", encoding="utf-8")
#fhandle5.close()
#fhandle5a = open(filename5a,"w", encoding="utf-8")
#fhandle5a.close()
#fhandle6 = open(filename6,"w", encoding="utf-8")
#fhandle6.close()
#fhandle6a = open(filename6a,"w", encoding="utf-8")
#fhandle6a.close()





'''
========Modified version for France- this part is commented out (inactive)=========
#Get country urls
print('\n','Fetching country urls...','\n')
with open(filename4,"a") as flog:
	print('\n','Fetching country urls...','\n',file=flog)
sp.open_session_firefox()
sp.browser.get("https://www.booking.com/destination.fr.html")
urls_1=sp.scrape('a',{'class':'dest-sitemap__subsublist-link'})
urls_1=urls_1.now()
url_start=[]
url_a_city=[]
for x in urls_1:
	try:
		url_start.append(re.sub(r'(\?)(.+)','','https://www.booking.com'+str(x['href'])))
		with open(filename5,"a") as f5:
			print(re.sub(r'(\?)(.+)','','https://www.booking.com'+str(x['href'])),file=f5)
	except:
		url_start.append('https://www.booking.com'+str(x['href']))
		with open(filename5,"a") as f5:
			print('https://www.booking.com'+str(x['href']),file=f5)

sp.close_session()
sp.browser.quit()
with open(filename5a,"a") as f5a:
	print(url_start,file=f5a)
#Get city urls
def bookgeturlcity(x):
	timeout = time.time() + 60*5
	while True:
		if time.time() > timeout:
			raise Exception("Timeout (5 minutes)")
			break
		try:
			sp.browser.close()
			sp.browser.quit()
		except:
			pass
		sp.open_session_firefox()
		sp.browser.get(x)
		time.sleep(randint(5,10))
		urls_2=sp.scrape('a',{'class':'dest-sitemap__subsublist-link'})
		urls_2_vf=urls_2.now()
		try:
			test=urls_2_vf[0]['href']
		except:
			time.sleep(randint(10,15))
			continue
		for y in urls_2_vf:
			try:
				url_a_city.append(re.sub(r'(\?)(.+)','','https://www.booking.com'+str(y['href'])))
				with open(filename6,"a") as f6:
					print(re.sub(r'(\?)(.+)','','https://www.booking.com'+str(y['href'])),file=f6)

			except:
				url_a_city.append('https://www.booking.com'+str(y['href']))
				with open(filename6,"a") as f6:
					print('https://www.booking.com'+str(y['href']),file=f6)
		break

# Execute requests with 20 threads max
print('\n','Fetching city urls...','\n')
with open(filename4,"a") as flog:
	print('\n','Fetching city urls...','\n',file=flog)

with concurrent.futures.ProcessPoolExecutor(max_workers=25) as executor:
	future_to_url = {executor.submit(bookgeturlcity, url): url for url in url_start}
	for future in tqdm(concurrent.futures.as_completed(future_to_url),total=len(future_to_url)):
		url = future_to_url[future]
		try:
			data = future.result()
		except Exception as exc:
			with open(filename4,"a") as flog:
				print('%r generated an exception: %s' % (url, exc),file=flog)
		else:
			with open(filename4,"a") as flog:
				print('%r page is completed' % url,file=flog)
url_a_city=list(map(lambda x: x.replace('/destination',''),url_a_city))
url_a_city=list(map(lambda x: re.sub(r'(\?)(.+)','',x),url_a_city))
with open(filename6a,"a") as f6a:
	print(url_a_city,file=f6a)

continue_=input('\nContinue?\n')
========Modified version for France- this part is commented out (inactive)=========
'''

#Import flag_urls

cwd = os.getcwd()
url_folder=str(cwd)+r"/urls"
read_files_flag = glob.glob(url_folder+r"/booking_flag_url1*")
with open(url_folder+r'/booking_flag_url.txt','w') as fconsolidated:
	for file in read_files_flag:
		with open(file) as f:
			flags=f.readlines()
			flags=list(map(lambda x: x.strip(),flags))
			flags=list(filter(lambda x: 'www.booking.com/city' in x,flags))
			for url in flags:
				print(url, file=fconsolidated)

with open(url_folder+r'/booking_flag_url.txt','r') as fconsolidated:
	url_a_city=fconsolidated.readlines()

url_a_city=list(map(lambda x: x.strip(),url_a_city))
url_a_city=list(dict.fromkeys(url_a_city))



#Generate consolited log file

read_files_logs = glob.glob("logs1*")
with open("consolidatedlog.txt", "w") as outfile:
	for f in read_files_logs:
		with open(f, "r") as infile:
			outfile.write(infile.read())

#Import logs

flogname='consolidatedlog.txt'
with open(flogname) as flogdone:
	done_urls=flogdone.readlines()

done_urls=list(map(lambda x: x.strip(),done_urls))
done_urls=list(map(lambda x: x.replace('\\n',''),done_urls))
done_urls=list(filter(lambda x: 'page is completed' in x or "title^='Page suivante" in x, done_urls))
done_urls=list(map(lambda x: re.findall(r"'(.+)'",x)[0],done_urls))
done_urls=list(map(lambda x: x.strip(),done_urls))
done_urls=list(map(lambda x: x.replace('\\n',''),done_urls))
url_a_city=list(set(url_a_city)-set(done_urls))
url_a_city=sorted(url_a_city)



#Define subfunction
def urlfetch():
	object_=sp.scrape('a',{'class':'js-sr-hotel-link hotel_name_link url'})
	object_=object_.now()
	for a in object_:
		urlhotel='https://www.booking.com'+a['href'].strip()
		try:
			urlhotel=re.sub(r'(\?)(.+)\s(.+)','',urlhotel)
		except:
			pass
		with open(filename2,'a') as f2:
			f2.write(urlhotel)
			f2.write('\n')

# Define main function

def searchcityurl(x):
	try:
		for counter in range(5):
			try:
				time.sleep(2)
				sp.open_session_firefox()
				#sp.browser.set_window_size(1920, 1080)
				#sp.browser.execute_script("document.body.style.zoom='25%'")
				#sp.browser.execute_script("document.body.style.transform = 'scale(0.25)'")
				time.sleep(2)
				sp.change(x)
				time.sleep(2)
				break
			except:
				time.sleep(2)
				sp.browser.quit()
				time.sleep(2)
				'''
				PROCNAME = "geckodriver"
				for proc in psutil.process_iter():
					 if proc.name() == PROCNAME:
						  proc.kill()
						  '''
		#sp.browser.execute_script("document.body.style.zoom='25%'")
		time.sleep(1)
		c=sp.browser.find_elements_by_id('onetrust-reject-all-handler')
		try:
			c[0].click()
			time.sleep(1)
		except:
			pass
		time.sleep(1)
		a=sp.browser.find_elements_by_class_name('sb-searchbox__button ')
		sp.browser.execute_script("arguments[0].scrollIntoView();", a[0])
		a[0].click()
		time.sleep(1)
		try:
			b=sp.browser.find_elements_by_class_name('sorth1')
		except:
			b=sp.browser.find_elements_by_class_name('ski-accommodation__title')
		sp.browser.execute_script("arguments[0].scrollIntoView();", b[0])
		b[0].click()
		time.sleep(1)
		element_=sp.scrape('h1',{'class':'sorth1'})
		element_=element_.now()
		if len(element_)>0:
			element_=element_[0].text
			element_=element_.replace(' ','').strip()
			try:
				element_=element_.replace('\xa0','').replace(' ','').strip()
			except:
				pass
			element_c=re.findall(r"(\d+)",element_)
			element_c_seuil=int(element_c[0])
		elif len(element_)==0:
			element_=sp.scrape('h2',{'class':'ski-accommodation__title'})
			element_=element_.now()
			element_=element_[0].text
			element_=element_.replace(' ','').strip()
			try:
				element_=element_.replace('\xa0','').replace(' ','').strip()
			except:
				pass
			element_c=re.findall(r"(\d+)établissementstrouvés",element_)
			element_c_seuil=int(element_c[0])
		with open(filename4,"a") as flog:
			print(element_c_seuil," etablissements sur l'url: ",x)
			print(element_c_seuil," etablissements sur l'url: ",x,file=flog)
		#smallville=sp.scrape('span',{'class':'bui_font_strong'})
		#smallville=smallville.now()

		try:
			visio1=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
			sp.browser.execute_script("arguments[0].scrollIntoView();", visio1)
			visio1.click()
		except:
			pass
		try:
			visio2=sp.browser.find_element_by_xpath('//*[@id="filter_district"]/div[2]/button[1]')
			sp.browser.execute_script("arguments[0].scrollIntoView();", visio2)
			visio2.click()
		except:
			pass
		try:
			visio3=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
			sp.browser.execute_script("arguments[0].scrollIntoView();", visio3)
			visio3.click()
		except:
			pass

		if element_c_seuil<=1000:
			with open(filename4,"a") as flog:
				print('Fetching : ',x,'with less than 1000 results',file=flog)
			with open(filename3,'a') as f3:
				f3.write(x)
				f3.write('\n')
			urlfetch()
			time.sleep(1)
			for counter_refresh in range(5):
				try:
					element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
				except:
					try:
						sp.browser.refresh()
						time.sleep(2)
						element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
					except:
						continue
			try:
				time.sleep(2)
				click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
				sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
				click_element.click()
			except:
				browser.refresh()
				time.sleep(2)
				click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
				sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
				click_element.click()
			while True:
				try:
					url_0=str(sp.browser.current_url)
					urlfetch()
					time.sleep(1)
					timeout = time.time() + 45
					try:
						element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
					except:
						try:
							sp.browser.refresh()
							element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
						except:
							continue
					try:
						time.sleep(2)
						click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
						sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
						click_element.click()
					except:
						browser.refresh()
						time.sleep(2)
						click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
						sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
						click_element.click()
						#time.sleep(4)
						url_1=str(sp.browser.current_url)
				except:
					if len(sp.browser.find_elements_by_css_selector("[title^='Page suivante']"))>0:
						raise Exception("Failed at pressing next-page button-Timeout")
						break
					else:
						raise Exception("Failed at pressing next-page button-Button not present...Check for completion")
						break

				if url_0==url_1:
					break


		elif element_c_seuil>1000:
			sp.data()
			e1=str(sp.sopa.findAll('a',{'data-id':"class-1"}))
			e2=str(sp.sopa.findAll('a',{'data-id':"class-2"}))
			e3=str(sp.sopa.findAll('a',{'data-id':"class-3"}))
			e4=str(sp.sopa.findAll('a',{'data-id':"class-4"}))
			e5=str(sp.sopa.findAll('a',{'data-id':"class-5"}))
			e0=str(sp.sopa.findAll('a',{'data-id':"class-0"}))
			se1=sp.soup(e1,'html.parser')
			se2=sp.soup(e2,'html.parser')
			se3=sp.soup(e3,'html.parser')
			se4=sp.soup(e4,'html.parser')
			se5=sp.soup(e5,'html.parser')
			se0=sp.soup(e0,'html.parser')
			de1={'label':se1.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(se1.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_class"]/div[2]/a[1]'}
			de2={'label':se2.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(se2.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_class"]/div[2]/a[2]'}
			de3={'label':se3.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(se3.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_class"]/div[2]/a[3]'}
			de4={'label':se4.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(se4.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_class"]/div[2]/a[4]'}
			de5={'label':se5.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(se5.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_class"]/div[2]/a[5]'}
			de0={'label':se0.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(se0.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_class"]/div[2]/a[6]'}
			listetoiles=[de1,de2,de3,de4,de5,de0]
			nextetoiles=[]
			base1=sp.browser.current_url
			for z in listetoiles:
				sp.change(base1)

				try:
					visio1=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
					sp.browser.execute_script("arguments[0].scrollIntoView();", visio1)
					visio1.click()
				except:
					pass
				try:
					visio2=sp.browser.find_element_by_xpath('//*[@id="filter_district"]/div[2]/button[1]')
					sp.browser.execute_script("arguments[0].scrollIntoView();", visio2)
					visio2.click()
				except:
					pass
				try:
					visio3=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
					sp.browser.execute_script("arguments[0].scrollIntoView();", visio3)
					visio3.click()
				except:
					pass

				time.sleep(2)
				sp.data()
				elem = sp.browser.find_element_by_xpath(z['id'])
				sp.browser.execute_script("arguments[0].scrollIntoView();", elem)
				elem.click()
				time.sleep(2)
				if z['count']<=1000:

					with open(filename4,"a") as flog:
						options=z['label']
						print('Fetching : ',x,'with more than 1000 results',options, file=flog)
					with open(filename3,'a') as f3:
						f3.write(x)
						f3.write('\n')
					urlfetch()
					time.sleep(1)
					try:
						element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
					except:
						try:
							sp.browser.refresh()
							element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
						except:
							continue
					try:
						time.sleep(2)
						click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
						sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
						click_element.click()
					except:
						browser.refresh()
						time.sleep(2)
						click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
						sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
						click_element.click()

					while True:
						try:
							url_0=str(sp.browser.current_url)
							urlfetch()
							time.sleep(1)
							timeout = time.time() + 45
							try:
								element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
							except:
								try:
									sp.browser.refresh()
									element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
								except:
									continue
							try:
								time.sleep(2)
								click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
								sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
								click_element.click()
							except:
								browser.refresh()
								time.sleep(2)
								click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
								sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
								click_element.click()
							#time.sleep(4)
							url_1=str(sp.browser.current_url)
						except:
							if len(sp.browser.find_elements_by_css_selector("[title^='Page suivante']"))>0:
								raise Exception("Failed at pressing next-page button-Timeout")
								break
							else:
								raise Exception("Failed at pressing next-page button-Button not present...Check for completion")
								break

						if url_0==url_1:
							break
				if z['count']>1000:
					sp.data()
					base2=sp.browser.current_url
					types=sp.sopa.findAll('a',{'data-name':"ht_id"})
					typesh=[]
					for type in types:
						inception=sp.soup(str(type),'html.parser')
						case={'label':inception.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(inception.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_hoteltype"]/div[2]/a['+str(types.index(type)+1)+']'}
						typesh.append(case)
					for type in typesh:
						sp.change(base2)

						try:
							visio1=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
							sp.browser.execute_script("arguments[0].scrollIntoView();", visio1)
							visio1.click()
						except:
							pass
						try:
							visio2=sp.browser.find_element_by_xpath('//*[@id="filter_district"]/div[2]/button[1]')
							sp.browser.execute_script("arguments[0].scrollIntoView();", visio2)
							visio2.click()
						except:
							pass
						try:
							visio3=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
							sp.browser.execute_script("arguments[0].scrollIntoView();", visio3)
							visio3.click()
						except:
							pass

						time.sleep(2)
						elem_type = sp.browser.find_element_by_xpath(type['id'])
						sp.browser.execute_script("arguments[0].scrollIntoView();", elem_type)
						elem_type.click()
						time.sleep(2)
						if type['count']<=1000:

							with open(filename4,"a") as flog:
								options=z['label']+'//'+type['label']
								print('Fetching : ',x,options, file=flog)
							with open(filename3,'a') as f3:
								f3.write(x)
								f3.write('\n')
							urlfetch()
							time.sleep(1)
							try:
								element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
							except:
								try:
									sp.browser.refresh()
									element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
								except:
									continue
							try:
								time.sleep(2)
								click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
								sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
								click_element.click()
							except:
								browser.refresh()
								time.sleep(2)
								click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
								sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
								click_element.click()

							while True:
								try:
									url_0=str(sp.browser.current_url)
									urlfetch()
									time.sleep(1)
									timeout = time.time() + 45
									try:
										element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
									except:
										try:
											sp.browser.refresh()
											element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
										except:
											continue
									try:
										time.sleep(2)
										click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
										sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
										click_element.click()
									except:
										sp.browser.refresh()
										time.sleep(2)
										click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
										sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
										click_element.click()
									#time.sleep(4)
									url_1=str(sp.browser.current_url)
								except:
									if len(sp.browser.find_elements_by_css_selector("[title^='Page suivante']"))>0:
										raise Exception("Failed at pressing next-page button-Timeout")
										break
									else:
										raise Exception("Failed at pressing next-page button-Button not present...Check for completion")
										break

								if url_0==url_1:
									break

						if type['count']>1000:
							sp.data()
							base3=sp.browser.current_url
							locations=sp.sopa.findAll('a',{'data-name':"di"})
							districts=[]
							for loc in locations:
								inception2=sp.soup(str(loc),'html.parser')
								case2={'label':inception2.findAll('span',{'class':'filter_label'})[0].text.strip(),'count':int(inception2.findAll('span',{'class':'filter_count'})[0].text.strip()),'id':'//*[@id="filter_district"]/div[2]/a['+str(locations.index(loc)+1)+']'}
								#print(case2)
								districts.append(case2)
							for district in districts:
								#print(base3)
								sp.change(base3)

								try:
									visio1=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
									sp.browser.execute_script("arguments[0].scrollIntoView();", visio1)
									visio1.click()
								except:
									pass
								try:
									visio2=sp.browser.find_element_by_xpath('//*[@id="filter_district"]/div[2]/button[1]')
									sp.browser.execute_script("arguments[0].scrollIntoView();", visio2)
									visio2.click()
								except:
									pass
								try:
									visio3=sp.browser.find_element_by_xpath('//*[@id="filter_hoteltype"]/div[2]/button[1]')
									sp.browser.execute_script("arguments[0].scrollIntoView();", visio3)
									visio3.click()
								except:
									pass

								time.sleep(2)
								elem_district = sp.browser.find_element_by_xpath(district['id'])
								sp.browser.execute_script("arguments[0].scrollIntoView();", elem_district)
								elem_district.click()
								time.sleep(2)
								if district['count']<=1000:
									try:
										with open(filename4,"a") as flog:
											options=z['label']+'//'+type['label']+'//'+district['label']
											print('Fetching : ',x,options, file=flog)
										with open(filename3,'a') as f3:
											f3.write(x)
											f3.write('\n')
										urlfetch()
										time.sleep(1)
										try:
											element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
										except:
											try:
												sp.browser.refresh()
												element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
											except:
												continue
										try:
											time.sleep(2)
											click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
											sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
											click_element.click()
										except:
											sp.browser.refresh()
											time.sleep(2)
											click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
											sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
											click_element.click()

										while True:
											try:
												url_0=str(sp.browser.current_url)
												urlfetch()
												time.sleep(1)
												timeout = time.time() + 45
												try:
													element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
												except:
													try:
														sp.browser.refresh()
														element = WebDriverWait(sp.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']")))
													except:
														continue

												try:
													time.sleep(2)
													click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
													sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
													click_element.click()

												except:
													sp.browser.refresh()
													time.sleep(2)
													click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
													sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
													click_element.click()

												#time.sleep(4)
												url_1=str(sp.browser.current_url)
											except:
												if len(sp.browser.find_elements_by_css_selector("[title^='Page suivante']"))>0:
													raise Exception("Failed at pressing next-page button-Timeout")
													break
												else:
													raise Exception("Failed at pressing next-page button-Button not present...Check for completion")
													break
											if url_0==url_1:
												break
									except:
										options=z['label']+'//'+type['label']+'//'+district['label']
										print('Problem with',x,'options:',options)
										continue



								if district['count']>1000:
									with open(filename4,"a") as flog:
										options=z['label']+'//'+type['label']+'//'+district['label']
										print('More than 1000 : ',x,options, file=flog)
									with open(filename3,'a') as f3:
										f3.write(x)
										f3.write('\n')
									continue
	except:
		#sp.close_session()
		sp.browser.quit()
		with open(filename4,"a") as flog:
			#print('\n','Fetching individual urls...','\n',file=flog)
			print('Did not complete:',x,file=flog)


	#sp.close_session()
	sp.browser.quit()

# Run algorithm 30 concurrent browsers


print('\n','Fetching individual urls...','\n')
with open(filename4,"a") as flog:
	print('\n','Fetching individual urls...','\n',file=flog)


with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
	future_to_url = {executor.submit(searchcityurl, url): url for url in url_a_city}
	for future in tqdm(concurrent.futures.as_completed(future_to_url),total=len(future_to_url)):
		url = future_to_url[future]
		try:
			data = future.result()
		except Exception as exc:
			with open(filename4,"a") as flog:
				print('%r generated an exception: %s' % (url, exc),file=flog)
		else:
			with open(filename4,"a") as flog:
				print('%r page is completed' % url,file=flog)
