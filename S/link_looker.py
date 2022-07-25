# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:17:54 2022

@author: Charles.Ferguson
"""

import requests, os, re
from bs4 import BeautifulSoup
validdirs = ['wps', 'Internet']
url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/class/?cid=nrcs142p2_053559'
linkd = {}
n=1

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

meat = soup.find(id='detail')

links = meat.find_all('a', href=True)

if not links is None:
    
    for l in links:
        
        # get the destination destination (href)
        link = l['href']
        
        # get the text on top of the hyperlink
        desc = l.get_text()
        desc = re.sub(r'[^A-Za-z0-9 ]+', '', desc)
        
        if desc == '':
            desc = 'Unhandled_link_text'
        
        print(link, desc)
        
        # filter more to make sure it's a vaild URL (not email, anchor,..)
        if link.find('/') != -1:
            
            baseh = os.path.basename(link)
            if baseh.find(".") != -1 or baseh.find("&ext=") != -1:
                
                # split on / to see if the
                # 2nd item is in ['wps', 'Internet']
                # these are 'our' links
                spl = link.split("/")
                
                
                # if it is, lets dl (download) the content
                # some of our content is not sourced relative i.e.
                # the download link has 'https://www.nrcs.usda.gov/
                if len(spl)>=4:
                    if spl[1] in validdirs or spl[3] in validdirs:
                        
                        # if not link.startswith('https://www.nrcs.usda.gov/'):
                        if not link.startswith('http'):
                            dl = 'https://www.nrcs.usda.gov' + link
                        else:
                            dl = link
                        
                        if desc in linkd:
                            desc = desc + '_v' + str(n)
                            linkd[desc] = dl
                            n+=1
                        else:
                            linkd[desc] = dl