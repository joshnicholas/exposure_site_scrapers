#%%

import requests 
import pandas as pd 
from bs4 import BeautifulSoup as bs 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox

chrome_options = Options()
chrome_options.add_argument("--headless")

#%%

sa = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/conditions/infectious+diseases/covid-19/testing+and+tracing/contact+tracing'

# r = requests.get(sa)
# soup = bs(r.text, 'html.parser')

options = Options()
options.add_argument("--headless")
driver = Firefox(options=options)
driver.get(sa)

soup = bs(driver.page_source.encode("utf-8"), 'html.parser')


#%%

# print(soup)

## TESTED AND QUARANTINE

content = soup.find("div",{"id":'scrollTo-Gettestedimmediatelyandquarantinefordayswithyourhousehold3'})

places = content.find_all("ul")
places = [x.text for x in places]

print(places)

# print(content)

# %%
