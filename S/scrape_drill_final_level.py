# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 08:20:44 2022

@author: Charles.Ferguson
"""

# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/survey/'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcs142p2_054261'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/geo/?cid=nrcseprd1423827'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/edu/?cid=stelprdb1236841'



def my_soup(address, dest):
    page = requests.get(address)
    # print(page.content)
    
    # parse the content and make it pretty 
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    
    # get the page tile to give substance to new folder name
    t = soup.find('title').get_text()
    t = re.sub(r'[^A-Za-z0-9 ]+', '', t).strip().replace(" ", "_")
    print(t)
    
    
    # use the base url as the name for a new folder to contain contnents
    newDir = re.sub(r'[^A-Za-z0-9 ]+', '', os.path.basename(address))
    
    # finally the new folder name
    folder =  t + "_" + newDir
    destination = os.path.join(root, folder)
    if not os.path.exists(destination):
        os.mkdir(destination)
    
        return True, soup, destination
    
    else:
        
        return False, None, None

def scrape_files(requester, edible, dest, dig=False):
    
    try:
        embeded = list()
        base = 'https://www.nrcs.usda.gov'
        # locations where documents/files are stored in WCT
        # start with either wps or Internet
        # this will filter things out like links to email
        content = ['wps', 'Internet']
        
        # test to determine if the page is type overview or detail
        divs = ("overview", "detail")
        for div in divs:
            
            meat = edible.find(id = div)
            # print(meat)
            
            if not meat is None:
                
                #  write the text in the div id to file
                meat_text = meat.get_text()
                meat_text = re.sub(r'\n+', '\n', meat_text).strip()
                # meat = re.sub(r"''", "'\n'", meat)
                
                with open(dest + os.sep + 'page_dialog.txt', 'w') as f:
                    f.write(meat_text)
                f.close()
                
                with open(dest + os.sep + 'page_dialog.html', 'w') as f:
                    f.write(str(meat))
                f.close()
            
                links = meat.find_all('a', href=True)
                # print(links)
                
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
                            print(requester + ":" + dl + "-" + desc)
                            
                            # if requester == 'top level' or (requester == 'second level' and link.find("?cid=") == -1):
                            if (requester == 'top level' or requester == 'second level') or (requester == 'final level' and (link.find(".") > 0 or link.find("&ext=") > 0)):
                                try:
                                    # time.sleep(1)
                                    response = requests.get(dl)
                                    
                                    # lets look at base url
                                    # if it has a . then it's a file
                                    # of some sort, lets get it
                                    bn = os.path.basename(dl)
                                    loc = bn.rfind(".")
                                    eloc = bn.rfind("&ext=")
                                    ref = bn.startswith('?cid=')
                                    if loc != -1:
                                        # print(dl, desc)
                                        print('\tdownloading a "." file')
                                        ext = bn[loc:]
                                        target = os.path.join(dest, desc.replace(" ", "_") + ext)
                                        if os.path.exists(target):
                                            target = os.path.join(dest, desc.replace(" ", "_") + '_v' + str(n) + ext)
                                            n+=1
                                        # print(target)
                                        open(target, "wb").write(response.content)
                                        print('\n\n')
                                    
                                   
                                    # if no ., then look for 
                                    # extension ("&ext=")
                                    elif eloc != -1:
                                        # print(dl, desc)
                                        print('\tdownloading a "ext" file')
                                        ext = bn[eloc + 5:]
                                        target = os.path.join(dest, desc.replace(" ", "_") + "." + ext)
                                        if os.path.exists(target):
                                            target = os.path.join(dest, desc.replace(" ", "_") + 'v' + str(n) + ext)
                                            n+=1
                                        open(target, "wb").write(response.content)
                                        print('\n\n')
                                        
                                    else:
                                        if dig == True:
                                            if ref != -1:
                                            
                                                if not link.startswith('http'):
                                                    print('\tcollecting for drill down')
                                                    embeded.append(base + link)
                                                else:
                                                    embeded.append(link)
                                except:
                                    fail.append(dl)
                            
                            else:
                                print('Skipping ' + requester + " " + dl)
            
                imgs = meat.find_all('img')
                
                if not imgs is None:
                    
                    for img in imgs:
                    
                        name = img.get('alt')
                        src = img.get('src')
                        
                        if src.find('/') != -1:
                            
                            # split on / to see if the
                            # 2nd item is in ['wps', 'Internet']
                            ispl = src.split("/")
                            
                            # if it is, lets dl (download) the content
                            # some of our content is not sourced relative i.e.
                            # the download link has 'https://www.nrcs.usda.gov/
                            if ispl[1] in content or ispl[3] in content:
                                
                                
                                # if not link.startswith('https://www.nrcs.usda.gov/')
                                if not link.startswith('http'):
                                    idl = 'https://www.nrcs.usda.gov/' + src
                                else:
                                    idl = src
                                    
                                response = requests.get(idl)
                                indext = src.rfind(".")
                                iext = src[indext:]
                                itarget = os.path.join(dest, name.replace(" ", "_") + iext)
                                open(itarget, "wb").write(response.content)
                        
            
        if dig == True:
            return True, embeded
                
        else:
            return False, None
    
    except requests.exceptions.RequestException as e:
        print(e)
        # msg = e.msg
        # print('Requests error: ' + msg)
        
# =============================================================================

import requests, os, re, pandas as pd
from bs4 import BeautifulSoup

# # local directory to store content
# each page scraped has folder created here
# root = r'D:\GIS\PROJECT_22\SCRAPE\DOC'
root = '/media/c/TRANSCEND_MOBI/nrcs'


# excel spreadsheet of urls
# f = r"D:\GIS\PROJECT_22\SCRAPE\T\Analytics All Web Site Data Event Pages 20180101-20220626-page-and-pagetitle.xlsx"
f = '/home/c/Documents/GitHub/SCRAPE/T/Analytics All Web Site Data Event Pages 20180101-20220626-page-and-pagetitle.xlsx'
df = pd.read_excel(f, sheet_name='Chad-downloads')

urls = df['CURL'].unique().tolist()

urls = urls[1:2]

fail = list()
haveurl = list()

try:
    for url in urls:
    
        soup1, soup, dest = my_soup(url, root)
        
        if soup1:
    
            topLevel, topval = scrape_files("top level", soup, dest, dig=True)
    
            if topLevel:
            
                if len(topval) > 0:
                
                    # here    
                    topval = topval[0:1]
                    
                    for nexturl in topval:
                
                        soup2, nextsoup, nextdest = my_soup(nexturl, root)
                
                        if soup2:
                            
                            nextlevel, nextval = scrape_files("second level", nextsoup, nextdest, dig=True)
                    
                            # ========================
                    
                            if nextlevel:
                            
                                if len(nextval) > 0:
                                
                                    for finalurl in nextval:
                                
                                        soup3, finalsoup, finaldest = my_soup(finalurl, root)
                                    
                                        if soup3:
                                            
                                            finallevel, finalval = scrape_files("final level", finalsoup, finaldest, dig=False)
                                            
                                        else:
                                            print('Running final level aready have: ' + finalurl)
                                            haveurl.append(finalurl)
                        else:
                            print('Running next level aready have: ' + nexturl)
                            haveurl.append(nexturl)
        else:
            print('Running top level aready have: ' + url)
            haveurl.append(url)                    
        
            
except:
    fail.append(url)

# urls = urls[:5]
# for url in urls:
    
#     try:
#         scrape(url)
#     except:
#         fail.append(url)

print('\nThese URLS were tried more than once')
for h in haveurl:
    print(h)

print('\nThe following urls failed')        
for f in fail:
    print(f)
