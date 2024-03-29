# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 07:41:25 2022

@author: Charles.Ferguson
"""

import requests, os, pandas as pd, re, traceback
from bs4 import BeautifulSoup

# # local directory to store content
# each page scraped has folder created here
root = r'D:\GIS\PROJECT_22\SCRAPE_temp'
# root = '/media/c/TRANSCEND_MOBI/nrcs'
validdirs = ['wps', 'Internet']
fail = list()

# excel spreadsheet of urls===================================
# f = r"D:\GIS\PROJECT_22\SCRAPE\T\Analytics All Web Site Data Event Pages 20180101-20220626-page-and-pagetitle.xlsx"
# f = '/home/c/Documents/GitHub/SCRAPE/T/Analytics All Web Site Data Event Pages 20180101-20220626-page-and-pagetitle.xlsx'
# f = r"D:\GIS\PROJECT_22\SCRAPE\T\03 - Soils - Content Worksheet.xlsx"
# df = pd.read_excel(f, sheet_name='scrape')
# df['Action'] = df['Action'].fillna('NA')
# df['Action'] = df['Action'].str.replace('?', "Unk")


# df = df[(df['Action'] == 'Keep')]


# urls = df['URL'].tolist()

# start = 200
# finish = len(urls)
# ndx = str(start) + '_' + str(finish)
# urls = urls[start:finish]




# test urls===============================================
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/use/','https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/use/urban/?cid=nrcs142p2_053986']           
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/survey/']
# urls = ["https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/use/worldsoils/edu/"]
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/soilsurvey/soils/survey/state/']
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/use/worldsoils/']
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcseprd1652414']
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/research/report/', 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/research/?cid=nrcs142p2_054275']
# urls = ['https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/edu/ncss/?cid=nrcs142p2_054322']

# urls from clipboard=======================================
# df = pd.read_clipboard("\t", header = None)
# urls = df[1].to_list()
# urls = urls[0:1]

urls_file = pd.read_csv(r'C:\temp\links_to_scrape.txt', sep ='\t')
urls = urls_file['URL'].unique().tolist()
start = 0
finish = len(urls)
ndx = str(start) + '_' + str(finish)
urls = urls[start:finish]

with open(os.path.join(root, 'log_' + ndx + '.log'), 'a') as lg:
    for url in urls:
        try:
            linkd = dict()
            n=1
            page = requests.get(url)
            # print(page.content)
            
            # parse the content and make it pretty 
            soup = BeautifulSoup(page.content, "html.parser")
            # print(soup)
            
            # get the page tile to give substance to new folder name
            t = soup.find('title').get_text()
            t = re.sub(r'[^A-Za-z0-9 ]+', '', t).strip().replace(" ", "_")
            lg.write(t + ": " + url + '\n')
            print(t)
            
            
            # use the base url as the name for a new folder to contain contnents
            newDir = re.sub(r'[^A-Za-z0-9 ]+', '', os.path.basename(url))
            # finally the new folder name
            folder =  t + "_" + newDir
            print('\t' + t + folder)
            destination = os.path.join(root, folder)
            dlen = len(destination)
            if not os.path.exists(destination):
                os.mkdir(destination)
                
                divs = ("overview", "detail", 'soilsurvey')
                
                for div in divs:
                    
                    if soup.find(id = div):
                        
                        meat = soup.find(id = div)
                        
                        #  write the text in the div id to file
                        meat_text = meat.get_text()
                        meat_text = re.sub(r'\n+', '\n', meat_text).strip()
                        # meat = re.sub(r"''", "'\n'", meat)
                        
                        with open(destination + os.sep + 'page_dialog.txt', encoding='utf-8', mode='w') as f:
                            f.write(meat_text)
                        f.close()
                        
                        with open(destination + os.sep + 'page_dialog.html', encoding='utf-8', mode='w') as f:
                            f.write(str(meat))
                        f.close()
                        
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
                                elif dlen + len(desc) > 250:
                                    desc = 'long_name'
                                
                                # print(link, desc)
                                
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
                                                
                                
                        imgs = meat.find_all('img')
                        
                        if not imgs is None:
                            
                            for img in imgs:
                                
                                src = img.get('src')
                                
                                if src.find('/') != -1:
                                    name = img.get('name')
                                    alt = img.get('alt')
                                    
                                    if name is not None:
                                        d = name
                                    elif alt is not None:
                                        d = alt


                                    if not d is None and (dlen + len(d)) > 250:
                                        d = 'long_name'
                                        
                                    if d is None:
                                        try:
                                            d = src.split(".")[0]
                                        except:
                                            d ='Unknown_content_type'
                
                                    d = re.sub(r'[^A-Za-z0-9 ]+', '', d)
                                    
                                    # if not link.startswith('https://www.nrcs.usda.gov/')
                                    # if not link.startswith('http'):
                                   
                                    
                                    # split on / to see if the
                                    # 2nd item is in ['wps', 'Internet']
                                    ispl = src.split("/")
                                    
                                    # if it is, lets dl (download) the content
                                    # some of our content is not sourced relative i.e.
                                    # the download link has 'https://www.nrcs.usda.gov/
                                    if len(ispl)>=4:
                                        if ispl[1] in validdirs or ispl[3] in validdirs:
                                            
                                            if not src.startswith('http'):
                                                idl = 'https://www.nrcs.usda.gov' + src
                                            else:
                                                idl = src
                                            
                                            if d in linkd:
                                                d = d + '_v' + str(n)
                                                linkd[d] = idl
                                                n+=1
                                            else:                                            
                                                linkd[d] = idl
                    else:
                        pass                                                                
            
                if len(linkd) > 0:
                
                    for desc in linkd:
                        
                        thelink = linkd.get(desc)
                        baselink = os.path.basename(thelink)
                        prdloc = baselink.rfind(".")
                        extloc = baselink.rfind("&ext=")
                        
                        if prdloc != -1:
                            # print('\t\tsub:  ' + thelink)
                            # print('\t\t\t' + desc)
                            response = requests.get(thelink)
                            extension = baselink[prdloc:]
                            target = os.path.join(destination, desc.replace(" ", "_") + extension)
                            if os.path.exists(target):
                                 target = os.path.join(destination, desc.replace(" ", "_") + '_v' + str(n) + extension)
                                 n+=1
                            open(target, "wb").write(response.content)
                         
                        if extloc != -1:
                            # print('\t\tsub:  ' + thelink)
                            # print('\t\t\t' + desc)
                            response = requests.get(thelink)
                            extension = baselink[extloc + 5:]
                            target = os.path.join(destination, desc.replace(" ", "_") + "." + extension)
                            if os.path.exists(target):
                                target = os.path.join(destination, desc.replace(" ", "_") + '_v' + str(n) + "." + extension)
                                n+=1
                            open(target, "wb").write(response.content)    
                    
                    
                    
                    
                else:
                    msg = '\tNo further links to grab'
                    lg.write(msg + '\n')
                    print(msg)
            else:
                msg = ('\tDirectory already exists for this URL')
                print(msg)
                lg.write(msg + '\n')
                with open(os.path.join(root, 'duplicate_urls_' + ndx + '.txt'), 'a') as d:
                    d.write(folder + ":" + url + '\n')
                d.close()
        except Exception as e:
            msg = ('\tURL fail: ' + url )
            print(msg)
            traceback.print_exc()
            lg.write('URL fail: ' + url + '\n')
            lg.write('\t' + str(e) + '\n')
            fail.append(url)
    with open(os.path.join(root, 'failed_urls_' + ndx + '.txt'), 'a') as f:
        for u in fail:
            f.write(u + '\n')
    f.close()
lg.close()