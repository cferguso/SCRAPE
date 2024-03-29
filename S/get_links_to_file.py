# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:57:22 2022

@author: Charles.Ferguson
"""

import requests, os, pandas as pd, re
from bs4 import BeautifulSoup

destination = r'C:\temp\links_to_scrape.txt'
url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/edu/ncss/?cid=nrcs142p2_054322'
validdirs = ['wps', 'Internet']
# print("state" + '\t' + 'CURL')
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

with open(destination, 'w') as f:
    f.write('description' + "\t" + "URL" +'\n')
    divs = ("overview", "detail", 'soilsurvey')
    
    
    for div in divs:
        
        if soup.find(id = div):
            meat = soup.find(id = div)
            links = meat.find_all('a', href=True)
            
            if not links is None:
                # print('state' + '\t' + 'url')
                for l in links:
                    
                    
                    # get the destination destination (href)
                    link = l['href']
                    
                    # split on / to see if the
                    # 2nd item is in ['wps', 'Internet']
                    # these are 'our' links
                    spl = link.split("/")
                    
                    
                    # if it is, lets dl (download) the content
                    # some of our content is not sourced relative i.e.
                    # the download link has 'https://www.nrcs.usda.gov/
                    if len(spl)>=4:
                        if spl[1] in validdirs or spl[3] in validdirs:
                            
                            base = os.path.basename(link)
                            if base.startswith('?cid=nrcs'):
                                desc = l.get_text()
                                desc = re.sub(r'[^A-Za-z0-9 ]+', '', desc)
                                if not link.startswith('http'):
                                    dl = 'https://www.nrcs.usda.gov' + link
                                else:
                                    dl = link
                                
                                f.write(desc + '\t' + dl + '\n')                        
        else:
            pass
            #print('Nothing')
f.close()      