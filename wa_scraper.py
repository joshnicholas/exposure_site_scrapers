import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from requests.packages import urllib3

urllib3.disable_warnings()

data_endpoint = "data/wa_exposure_sites.csv"

urlo = 'https://healthywa.wa.gov.au/Articles/A_E/Coronavirus/Locations-visited-by-confirmed-cases'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(urlo, headers=headers, verify=False)
html = r.text

## GRAB THE HEADLINES FROM THE COLLAPSABLE BUTTONS
soup = bs(html, 'html.parser')
callums = soup.find_all(class_="doh-accordian_btn")
callums = [x.text for x in callums]
callums = [x.replace("Public exposure sites – ", '') for x in callums]
callums = [x.strip() for x in callums]

callums = [x for x in callums if x.lower() != "flights"]

tables = pd.read_html(html)

listo = []

for i in range(0,len(callums)):
    table = tables[i].copy()

    if table.columns[0] == 0:
        table.columns = table.iloc[0]
        table = table[1:]

    table['Health advice'] = callums[i]

    listo.append(table)

final = pd.concat(listo)

final['Date'] = pd.to_datetime(final['Date'])

final = final.sort_values(by="Date", ascending=False)
final['Date'] = final['Date'].dt.strftime('%d/%m/%Y')

df = final 

old = pd.read_csv(data_endpoint)

combo = old.append(df)

combo = combo.drop_duplicates(subset=['Location', 'Address', 'Date', 'Time'])

with open(data_endpoint, "w") as f:
    combo.to_csv(f, index=False, header=True)