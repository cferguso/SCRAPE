# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 13:57:46 2022

@author: Charles.Ferguson
"""

import requests, os, re
from bs4 import BeautifulSoup

# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/survey/'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcs142p2_054261'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/getelpro/?cid=nrcseprd1423827'
# url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/edu/?cid=sdb1236841'
url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/main/soils/use/urban/'
page = requests.get(url)

# print(page.content)

# use the base url as the name for a new folder to contain contnents
newDir = re.sub(r'[^A-Za-z0-9 ]+', '', os.path.basename(url))

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
    
    # if meat is not None:
    #     meat_text = meat.get_text()
    #     meat_text = re.sub(r'\n+', '\n', meat_text).strip()
    #     # meat = re.sub(r"''", "'\n'", meat)
    #     with open(destination + os.sep + 'meat.txt', 'w') as f:
    #         f.write(meat_text)
    #     f.close()
    #     print(meat)
    if not meat is None:
        imgs = meat.find_all('img')
        for img in imgs:
            print(img)
            # name = img.get('alt')
            # src = img.get('src')
            
            
        
    else:
        pass
