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
    print('\t' + t)
    
    
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

def genpage(soup, dest):
    
    divs = ("overview", "detail")
    
    try:
        
        for div in divs:
            
            meat = soup.find(id = div)
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
        
                return True, meat
    
    except:
        
        return False, None


def getlinks(meat):
    # print(meat)
    linkd = dict()
    links = meat.find_all('a', href=True)
    
    if not links is None:
        
        for l in links:
            
            # get the destination destination (href)
            link = l['href']
            
            # get the text on top of the hyperlink
            desc = l.get_text()
            desc = re.sub(r'[^A-Za-z0-9 ]+', '', desc)
            
            # print(link, desc)
            
            # filter more to make sure it's a vaild URL (not email, anchor,..)
            if link.find('/') != -1:
                
                # if not link.startswith('https://www.nrcs.usda.gov/'):
                if not link.startswith('http'):
                    dl = 'https://www.nrcs.usda.gov' + link
                else:
                    dl = link
                
                # split on / to see if the
                # 2nd item is in ['wps', 'Internet']
                # these are 'our' links
                spl = link.split("/")
                print(spl)
                
                # if it is, lets dl (download) the content
                # some of our content is not sourced relative i.e.
                # the download link has 'https://www.nrcs.usda.gov/
                if spl[1] in validdirs or spl[3] in validdirs:
                    linkd[desc] = dl
            
    imgs = meat.find_all('img')
    
    if not imgs is None:
        
        for img in imgs:
            
            src = img.get('src')
            name = img.get('name')
            alt = img.get('alt')
            
            if name is not None:
                d = name
            elif alt is not None:
                d = alt
                
            if d is None:
                try:
                    d = src.split(".")[0]
                except:
                    d ='Unknown_content_type'

                        
            src = img.get('src')
            
            if src.find('/') != -1:
                
                # if not link.startswith('https://www.nrcs.usda.gov/')
                # if not link.startswith('http'):
                if not src.startswith('http'):
                    idl = 'https://www.nrcs.usda.gov' + src
                else:
                    idl = src
                
                # split on / to see if the
                # 2nd item is in ['wps', 'Internet']
                ispl = src.split("/")
                
                # if it is, lets dl (download) the content
                # some of our content is not sourced relative i.e.
                # the download link has 'https://www.nrcs.usda.gov/
                if ispl[1] in validdirs or ispl[3] in validdirs:
                    
                    linkd[d] = idl
                                                            
    if len(linkd) > 0:
        return True, linkd
    
    else:
        msg = 'No further links to grab'
        return False, msg
    
               
                
import requests, os, re, pandas as pd, traceback
from bs4 import BeautifulSoup

# # local directory to store content
# each page scraped has folder created here
root = r'D:\GIS\PROJECT_22\SCRAPE_RESULTS'
# root = '/media/c/TRANSCEND_MOBI/nrcs'
validdirs = ['wps', 'Internet']

# excel spreadsheet of urls
f = r"D:\GIS\PROJECT_22\SCRAPE\T\Analytics All Web Site Data Event Pages 20180101-20220626-page-and-pagetitle.xlsx"
# f = '/home/c/Documents/GitHub/SCRAPE/T/Analytics All Web Site Data Event Pages 20180101-20220626-page-and-pagetitle.xlsx'
df = pd.read_excel(f, sheet_name='Chad-downloads')

urls = df['CURL'].unique().tolist()

urls = urls[:25]

# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/use/','https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/use/urban/?cid=nrcs142p2_053986']           
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/survey/']
# urls = ["https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/use/worldsoils/edu/"]
for url in urls:
   
   try:
       print('\tSS URL: ' +  url)
       # take orginal url, generate soup, create a dir
       toplogic, topsoup, topdest = my_soup(url, root)
       
       if toplogic:
           # get to the relevant content
           genbool, edible = genpage(topsoup, topdest)
           
           
           if genbool:
               # get the links both URL and files
               
               getbool, linkval = getlinks(edible)
               
               if getbool: 
                   n=1
                   for desc in linkval:
                       
                       thelink = linkval.get(desc)
                       baselink = os.path.basename(thelink)
                       prdloc = baselink.rfind(".")
                       extloc = baselink.rfind("&ext=")
                       
                       if prdloc != -1:
                           print('\t\tsub:  ' + thelink)
                           print('\t\t\t' + desc)
                           response = requests.get(thelink)
                           extension = baselink[prdloc:]
                           target = os.path.join(topdest, desc.replace(" ", "_") + "." + extension)
                           if os.path.exists(target):
                                target = os.path.join(topdest, desc.replace(" ", "_") + '_v' + str(n) + "." + extension)
                                n+=1
                           open(target, "wb").write(response.content)
                        
                       if extloc != -1:
                           print('\t\tsub:  ' + thelink)
                           print('\t\t\t' + desc)
                           response = requests.get(thelink)
                           extension = baselink[extloc + 5:]
                           target = os.path.join(topdest, desc.replace(" ", "_") + "." + extension)
                           if os.path.exists(target):
                               target = os.path.join(topdest, desc.replace(" ", "_") + '_v' + str(n) + "." + extension)
                               n+=1
                           open(target, "wb").write(response.content)
                    
               else:
                   print(linkval + " for " + url)
           else:
                print("Could not create local page for: " + url)
       else:
            print("Either could not read or dir existed from: " + url)
   except:
       print("\n\n")
       traceback.print_exc()
       print('\t\t\tURL simply did not run, possibly no internal links')
       print("\n\n")