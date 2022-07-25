# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:38:49 2022

@author: Charles.Ferguson
"""

import pandas as pd
ss= r"D:\GIS\PROJECT_22\SCRAPE\T\03 - Soils - Content Worksheet.xlsx"
urls = pd.read_excel(ss, 'scrape')
dup = urls.duplicated(subset=['Page Title', 'URL'])
res = urls.loc[dup, :]

u_dup = urls['URL'].duplicated()
u_sum =(urls['URL'].duplicated()).sum()

t_dup = urls['Page Title'].duplicated
t_sum =(urls['Page Title'].duplicated()).sum()

titles = urls.loc[urls['Page Title'].duplicated()]
titles.sort_values('Page Title', axis = 0, inplace = True)
