# -*- coding: utf-8 -*-

# Importing modules

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import concurrent.futures
import requests
from bs4 import BeautifulSoup as soup
import time
import re
import os
import json
import pandas as pd
import datetime
import glob

# Setting up proxy
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
http_proxy = "http://127.0.0.1:24000"
https_proxy = "https://127.0.0.1:24000"
ftp_proxy = "ftp://127.0.0.1:24000"
proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "ftp"   : ftp_proxy
            }



# Setting up the list of URLs

#fname = input('\nPlease enter the name of the text file with the Booking URLs\n')
fname = '/Bookinfo/urls/booking_url.txt'

with open(fname) as handle:
    urls= handle.readlines()

urls = list(dict.fromkeys(urls))


#Setting log files

timestamp=int(time.time())
flogname="logs"+str(timestamp)+".txt"
flogfile = open(flogname,"w", encoding="utf-8")
now = datetime.datetime.now()
print (now.strftime("%Y-%m-%d %H:%M:%S"),file=flogfile)
flogfile.close()

#Generate consolited log file

read_files = glob.glob("logs1*")
with open("consolidatedlog.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())


#Import logs

cflogname='consolidatedlog.txt'
with open(cflogname) as flogdone:
    done_urls=flogdone.readlines()

done_urls=list(filter(lambda x: 'page is completed' in x , done_urls))
done_urls=list(map(lambda x: re.findall(r"'(.+)'",x)[0],done_urls))
url_hotel=list(set(urls)-set(done_urls))
url_hotel=sorted(url_hotel)
url_hotel=list(map(lambda x: x.strip(),url_hotel))



# Setting up of CSV file
timestamp=int(time.time())
filename = "booking"+str(timestamp)+".csv"
fhandle = open(filename,"w", encoding="utf-8")
headers = "url; name; description; review; score; number of reviews; type of property; address; stars; recommend; descdetail; equip; equipdetail; lat; long; hotelchain; type2\n"
fhandle.write(headers)
fhandle.close()

# Definition of the crawl function
def bookcrawl(url):
    with open(flogname,"a") as flogfile:
        print(url,file=flogfile)
    # Opening webpage and parsing of html
    r=requests.get(url, proxies=proxyDict, verify=False)
    book_soup = soup(r.text, "html.parser")

    #Generate address variable
    address = book_soup.findAll("span", {"class":"hp_address_subtitle"})
    try:
        cleanaddress = address[0].text.strip()
    except:
        cleanaddress = ""
    #Generate stars variable
    stars = book_soup.findAll("span", {"class":"hp__hotel_ratings__stars nowrap"})
    try:
        cleanstars = stars[0].text.strip()
    except:
        cleanstars = ""

    #Generate recommendation variable
    recom = book_soup.findAll("span", {"class":"facility-badge__tooltip-title"})
    try:
        cleanrom = recom[0].text.strip()
    except:
        cleanrom = ""

    #Generate Property description variable
    content = book_soup.findAll("div", {"id":"property_description_content"})
    try:
        cleancontent = content[0].text.strip().replace("\n"," ").replace(";",",")
    except:
        cleancontent = ""


    hname = book_soup.findAll("h2",{"id":"hp_hotel_name"})
    try:
        hname=str(hname[0].text.strip())
        posnewline=hname.find('\n')+1
        hname=hname[posnewline:]
    except:
        hname=''

    desc = container.findAll("div", {"class":"hotel_desc"})
    review = container.findAll("div", {"class":"bui-review-score__title"})

    try:
        cleandesc = desc[0].text.strip().replace(";",",")
    except:
        cleandesc = ""
    try:
        cleanreview = review[0].text.strip()
    except:
        cleanreview = ""
    badge = container.findAll("div", {"class":"bui-review-score__badge"})
    try:
        cleanbadge = badge[0].text.strip()
    except:
        cleanbadge = ""
    numreviews = container.findAll("div", {"class":"bui-review-score__text"})
    try:
        cleannumreviews = numreviews[0].text.strip()
    except:
        cleannumreviews = ""
    try:
        type = container.findAll("div", {"class":"bui-u-inline"})
        cleantype = type[0].text.strip()
    except:
        cleantype = ""
    try:
        equip = book_soup.findAll("div", {"class":"important_facility"})
        listequip = []
        for i in range(0,len(equip)):
            new = equip[i].text.strip().replace('\n','').replace('\r','')
            listequip.append(new)
            cleanequip = ','.join(listequip)
    except:
        cleanequip = ""
    try:
        equip2 = book_soup.findAll("div", {"class":"facilitiesChecklistSection"})
        listequip2 = []
        for i in range(0,len(equip2)):
            new = equip2[i].text.strip().replace('\n',',').replace('\r','')
            listequip2.append(new)
        cleanequip2 = ','.join(listequip2)
        cleanequip2 = replace(cleanequip2,',')

    except:
        cleanequip2 = ""
    try:
        comment = book_soup.findAll("span", {"class":"c-review__body"})
        listcomment = []
        for i in range(0,len(comment)):
            newc = comment[i].text.strip().replace('\n','').replace('\r','')
            listcomment.append(newc)
        cleancomment = ','.join(listcomment)
    except:
        cleancomment = ""

    poi2 = book_soup.findAll("div", {"class":"hp-poi-list__description"})
    poi3 = book_soup.findAll("span", {"class":"hp-poi-list__distance"})

    try:
        listpoi = []
        for i in range(0,len(poi2)):
            poi = poi2[i].text.strip().replace('\n','').replace('\r','')+" "+poi3[i].text.strip().replace('\n','').replace('\r','')
            listpoi.append(poi)
        cleanpoi = ' , '.join(listpoi)
    except:
        cleanpoi = ""

    # Generate location variables
    try:
        s=str(book_soup.findAll("a", {"id":"hotel_sidebar_static_map"}))
        text='data-atlas-latlng'
        a = s.find(text)
        e = a+42
        s2=s[a:e]
        s3 = re.sub('[^0-9,.]', "" , s2)
        z=s3.find(",")
        lat = s3[:z]
        long = s3[z+1:]

    except:
        lat=""
        long=""

    # Generate chain classification variable
    try:
        chain = book_soup.findAll("p", {"class":"summary hotel_meta_style"})
        cleanchain=chain[0].text.strip()
        schain=str(cleanchain)
        if schain.find("Chaîne hôtelière/marque:")==-1:
            schain=""
        else:
            xx = schain.find("Chaîne hôtelière/marque:")+len("Chaîne hôtelière/marque:")
            schain=schain[xx:].strip().replace("\n"," ").replace('\r',"")
    except:
        schain=""


    # Generate hotel type variable
    try:
        hbadge = book_soup.findAll("span", {"class":"hp__hotel-type-badge"})
        cleanhbadge = hbadge[0].text.strip()
    except:
        cleanhbadge = ""

    with open(filename,"a") as fhandle:
        fhandle.write(furl + ';' + hname + ';' + cleandesc + ';' + cleanreview + ';' + cleanbadge + ';' + cleannumreviews + ';' + cleantype + ';' + cleanaddress + ';' + cleanstars + ';' + cleanrom + ';' + cleancontent + ';' + cleanequip + ';' + cleanequip2 + ';' + lat + ';' + long + ';' + schain + ';' + cleanhbadge + '\n')


print('\n','Fetching individual urls...','\n')
with open(flogname,"a") as flogfile:
    print('\n','Fetching individual urls...','\n',file=flogfile)


with concurrent.futures.ProcessPoolExecutor(max_workers=7) as executor:
    future_to_url = {executor.submit(bookcrawl, url): url for url in url_hotel}
    for future in tqdm(concurrent.futures.as_completed(future_to_url),total=len(future_to_url)):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            with open(flogname,"a") as flogfile:
                print('%r generated an exception: %s' % (url, exc),file=flogfile)
        else:
            with open(flogname,"a") as flogfile:
                print('%r page is completed' % url,file=flogfile)
