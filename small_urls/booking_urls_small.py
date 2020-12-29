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

#Generate consolited log file

read_files = glob.glob("logs1*")
with open("consolidatedlog.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())

#Import French cities

with open('master_city_url_selection.txt') as fselection:
    url_a_city=fselection.readlines()

url_a_city=list(map(lambda x: x.strip(),url_a_city))

url_a_city=list(map(lambda x: x.replace('/destination',''),url_a_city))

#Import logs

flogname='consolidatedlog.txt'
with open(flogname) as flogdone:
    done_urls=flogdone.readlines()
  
done_urls=list(filter(lambda x: 'page is completed' in x or "title^='Page suivante" in x, done_urls))  
done_urls=list(map(lambda x: re.findall(r"'(.+)'",x)[0],done_urls))
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
    for counter in range(5):
        try:
            sp.open_session_firefox()
            break
        except:
            PROCNAME = "geckodriver"
            for proc in psutil.process_iter():
                 if proc.name() == PROCNAME:
                      proc.kill()  
    sp.change(x)
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
    b=sp.browser.find_elements_by_class_name('sorth1')
    sp.browser.execute_script("arguments[0].scrollIntoView();", b[0])
    b[0].click()
    time.sleep(1)
    element_=sp.scrape('h1',{'class':'sorth1'})
    element_=element_.now()
    element_=element_[0].text
    element_=element_.replace(' ','').strip()
    try:
        element_=element_.replace('\xa0','').replace(' ','').strip()
    except:
        pass
    element_c=re.findall(r"(\d+)",element_)
    element_c_seuil=int(element_c[0])
    with open(filename4,"a") as flog:
        print(element_c_seuil," etablissements sur l'url: ",x,file=flog)
    #smallville=sp.scrape('span',{'class':'bui_font_strong'})
    #smallville=smallville.now()
    if element_c_seuil>1000:
        with open(filename4,"a") as flog:
            print('Skipped :',x,file=flog)
        with open(filename,'a') as f:
            f.write(x)
            f.write('\n')
        sp.close_session()
        sp.browser.quit()
    elif element_c_seuil<=1000:
        with open(filename4,"a") as flog:
            print('Fetching : ',x,file=flog)
        with open(filename3,'a') as f3:
            f3.write(x)
            f3.write('\n')
        urlfetch()
        element = WebDriverWait(sp.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']"))) 
        click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
        sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
        click_element.click()
        while True:
            try:
                url_0=str(sp.browser.current_url)
                urlfetch()
                timeout = time.time() + 45
                element = WebDriverWait(sp.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Page suivante']"))) 
                click_element=sp.browser.find_element_by_css_selector("[title^='Page suivante']")
                sp.browser.execute_script("arguments[0].scrollIntoView();", click_element)
                click_element.click()
                time.sleep(4)
                url_1=str(sp.browser.current_url)       
            except:
                if len(sp.browser.find_elements_by_css_selector("[title^='Page suivante']"))>0:
                    sp.close_session()
                    sp.browser.quit()
                    raise Exception("Failed at pressing next-page button-Timeout")
                    break
                else:
                    sp.close_session()
                    sp.browser.quit()
                    raise Exception("Failed at pressing next-page button-Button not present...Check for completion")
                    break
                      
            if url_0==url_1:
                sp.close_session()
                sp.browser.quit()
                break

        
# Run algorithm 30 concurrent browsers 


print('\n','Fetching individual urls...','\n')
with open(filename4,"a") as flog:
    print('\n','Fetching individual urls...','\n',file=flog)


with concurrent.futures.ProcessPoolExecutor(max_workers=7) as executor:
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
