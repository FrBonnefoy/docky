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
from tqdm import tqdm

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

#Setting up file with done urls


fdonename="done"+str(timestamp)+".txt"
fdonefile = open(fdonename,"w", encoding="utf-8")
now = datetime.datetime.now()
print (now.strftime("%Y-%m-%d %H:%M:%S"),file=fdonefile)
fdonefile.close()

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
headers = "url\tname\tdescription\treview\tscore\tnumber of reviews\ttype of property\taddress\tstars\trecommend\tdescdetail\tequip\tequipdetail\tlat\tlong\thotelchain\trestaurant\tPOIs\tComments\n"
fhandle.write(headers)
fhandle.close()

# Definition of the crawl function
def bookcrawl(url):
    with open(flogname,"a") as flogfile:
        print("Fetching "+url,file=flogfile)
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
    stars = book_soup.findAll("span", {"class":"bui-rating bui-rating--smaller"})
    try:
        cleanstars = stars[0]['aria-label'].replace(' out of 5','')
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

    desc = book_soup.findAll("div", {"id":"summary"})
    review = book_soup.findAll("div", {"class":"bui-review-score__title"})

    try:
        cleandesc = desc[0].text.strip().replace("\n"," ")
    except:
        cleandesc = ""
    try:
        cleanreview = review[0].text.strip()
    except:
        cleanreview = ""
    badge = book_soup.findAll("div", {"class":"bui-review-score__badge"})
    try:
        cleanbadge = badge[0].text.strip().replace(',','.')
        cleanbadge=float(cleanbadge)
    except:
        cleanbadge = ""
    numreviews = book_soup.findAll("div", {"class":"bui-review-score__text"})
    try:
        cleannumreviews = numreviews[0].text.strip()
        cleannumreviews=re.findall(r'\d+',cleannumreviews)[0]
        cleannumreviews=int(cleannumreviews)
    except:
        cleannumreviews = ""
    try:
        type = book_soup.findAll("span", {"class":"hp__hotel-type-badge"})
        if len(type)>0:
            cleantype = type[0].text.strip()
        else:
            type = book_soup.findAll("span", {"class":"bui-badge bh-property-type bh-property-type--constructive-dark"})
            cleantype = type[0].text.strip()
    except:
        cleantype = ""
    try:
        equip = book_soup.findAll("div", {"class":"important_facility"})
        listequip = []
        for i in range(0,len(equip)):
            new = equip[i].text.strip().replace('\n','').replace('\r','')
            listequip.append(new)
            cleanequip = ' // '.join(listequip)
    except:
        cleanequip = ""
    try:
        equip2 = book_soup.findAll("div", {"class":"facilitiesChecklistSection"})
        listequip2 = []
        for i in range(0,len(equip2)):
            new = equip2[i].text.strip().replace('\n',',').replace('\r','')
            listequip2.append(new)
        cleanequip2 = ' // '.join(listequip2)
        cleanequip2=re.sub(r'(,+)',', ',cleanequip2).replace('\xa0!','')


    except:
        cleanequip2 = ""
    try:
        comment = book_soup.findAll("span", {"class":"c-review__body"})
        listcomment = []
        for i in range(0,len(comment)):
            newc = comment[i].text.strip().replace('\n','').replace('\r','').replace('\xa0','')
            listcomment.append(newc)
        cleancomment = ' // '.join(listcomment)
    except:
        cleancomment = ""

    inception = soup(str(book_soup.findAll("div", {"class":"hp_location_block__content_container"})),'html.parser')
    poi2=inception.findAll("div",{'class':'bui-list__description'})
    poi3 = inception.findAll("div",{'class':'bui-list__item-action hp_location_block__section_list_distance'})

    try:
        listpoi = []
        for i in range(0,len(poi2)):
            poi = poi2[i].text.strip().replace('\n','').replace('\r','')+" : "+poi3[i].text.strip().replace('\n','').replace('\r','')
            listpoi.append(poi)
        cleanpoi = ' // '.join(listpoi)
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

    restaurant=book_soup('div',{'class':'bui-grid bui-grid--bleed restaurant-block'})
    try:
        cleanrest='Nom:'+restaurant[0].text.replace('\n',' ').replace('\xa0','')
    except:
        cleanrest=''

    varlist=[url , hname , cleandesc , cleanreview , cleanbadge , cleannumreviews ,  cleantype , cleanaddress , cleanstars , cleanrom , cleancontent , cleanequip , cleanequip2 , lat , long , schain , cleanrest,cleanpoi,cleancomment ]
    to_append=varlist
    s = pd.DataFrame(to_append).T
    s.to_csv(filename, mode='a', header=False,sep='\t',index=False)

    with open(fdonename,"a") as f:
        print(url,file=f)
    #print(url)



print('\n','Fetching individual urls...','\n')

pbar=tqdm(total=len(url_hotel))

with open(flogname,"a") as flogfile:
    print('\n','Fetching individual urls...','\n',file=flogfile)


with concurrent.futures.ProcessPoolExecutor(max_workers=21) as executor:
    future_to_url = {executor.submit(bookcrawl, url): url for url in url_hotel}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            pbar.update(1)
        except Exception as exc:
            with open(flogname,"a") as flogfile:
                print('%r generated an exception: %s' % (url, exc),file=flogfile)
        else:
            with open(flogname,"a") as flogfile:
                print('%r page is completed' % url,file=flogfile)

pbar.close()
