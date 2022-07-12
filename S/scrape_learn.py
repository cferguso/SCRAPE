# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 08:20:44 2022

@author: Charles.Ferguson
"""

import requests, os, re
from bs4 import BeautifulSoup

# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/survey/'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcs142p2_054261'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/geo/?cid=nrcseprd1423827'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/edu/?cid=stelprdb1236841'

def scrape(address):
    page = requests.get(address)
    
    # print(page.content)
    
    # use the base url as the name for a new folder to contain contnents
    newDir = re.sub(r'[^A-Za-z0-9 ]+', '', os.path.basename(address))
    
    # parse the content and make it pretty 
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    
    # get the page tile to give substance to new folder name
    t = soup.find('title').get_text()
    t = re.sub(r'[^A-Za-z0-9 ]+', '', t).strip().replace(" ", "_")
    # print(t)
    
    # finally the new folder name
    folder =  t + "_" + newDir
    
    # local directory to store content
    root = r'D:\GIS\PROJECT_22\SCRAPE\DOC'
    destination = os.path.join(root, folder)
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    
    
    # test to determine if the page is type overview or detail
    divs = ("overview", "detail")
    for div in divs:
        
        meat = soup.find(id = div)
        # print(meat)
        
        if not meat is None:
            
            #  write the text in the div id to file
            meat_text = meat.get_text()
            meat_text = re.sub(r'\n+', '\n', meat_text).strip()
            # meat = re.sub(r"''", "'\n'", meat)
            with open(destination + os.sep + 'page_dialog.txt', 'w') as f:
                f.write(meat_text)
            f.close()
        
        
            links = meat.find_all('a', href=True)
            print(links)
            
            # locations where documents/files are stored in WCT
            # start with either wps or Internet
            # this will filter things out like links to email
            content = ['wps', 'Internet']
            
            n=1
            for a in links:
                
                # get the destination destination (href)
                link = a['href']
                
                # get the text on top of the hyperlink
                desc = a.get_text()
                desc = re.sub(r'[^A-Za-z0-9 ]+', '', desc)
                
                # print(link, desc)
                
                # filter more to make sure it's a vaild URL (not email, anchor,..)
                if link.find('/') != -1:
                    
                    # split on / to see if the
                    # 2nd item is in ['wps', 'Internet']
                    spl = link.split("/")
                    
                    # if it is, lets dl (download) the content
                    # some of our content is not sourced relative i.e.
                    # the download link has 'https://www.nrcs.usda.gov/
                    if spl[1] in content or spl[3] in content:
                        
                        
                        # if not link.startswith('https://www.nrcs.usda.gov/'):
                        if not link.startswith('http'):
                            dl = 'https://www.nrcs.usda.gov/' + link
                        else:
                            dl = link
                
                        # print(dl, desc)
                        response = requests.get(dl)
                        
                        # lets look at base url
                        # if it has a . then it's a file
                        # of some sort, lets get it
                        bn = os.path.basename(dl)
                        loc = bn.rfind(".")
                        if loc != -1:
                            print(dl, desc)
                            ext = bn[loc:]
                            target = os.path.join(destination, desc.replace(" ", "_") + ext)
                            if os.path.exists(target):
                                target = os.path.join(destination, desc.replace(" ", "_") + '_v' + str(n) + ext)
                                n+=1
                            # print(target)
                            open(target, "wb").write(response.content)
                            print('\n\n')
                        
                       
                        # if no ., then look for 
                        # extension ("&ext=")
                        else:
                            eloc = bn.rfind("&ext=")
                            if eloc != -1:
                                print(dl, desc)
                                ext = bn[eloc + 5:]
                                target = os.path.join(destination, desc.replace(" ", "_") + "." + ext)
                                if os.path.exists(target):
                                    target = os.path.join(destination, desc.replace(" ", "_") + 'v' + str(n) + ext)
                                    n+=1
                                open(target, "wb").write(response.content)
                                print('\n\n')


import requests, os, re,  pandas as pd
from bs4 import BeautifulSoup

# f = r"D:\GIS\PROJECT_22\SCRAPE\T\Analytics All Web Site Data Event Pages 20180101-20220626-page-and-pagetitle.xlsx"
# df = pd.read_excel(f, sheet_name='Chad-downloads')

# urls = df['URL'].unique().tolist()
urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/edu/?cid=stelprdb1236841']
fail = list()
# urls = urls[:5]
for url in urls:
    
    try:
        scrape(url)
    except:
        fail.append(url)
        
for f in fail:
    print(f)
