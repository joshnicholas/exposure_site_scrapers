import pandas as pd
import requests
import re

data_endpoint = "data/qld_exposure_sites.csv"

pd.set_option("display.max_rows", None, "display.max_columns", None)

headers = {'user-agent': 'The Guardian'}
html = requests.get('https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/contact-tracing', headers=headers).text
tables = pd.read_html(html)

table_labels = ["Close contacts", "Casual contacts", "Low risk contacts"]

listo = []
for i in range(0, len(table_labels)):
    inter = tables[i]
    inter['Type'] = table_labels[i]
    listo.append(inter)


df = pd.concat(listo)


df['Place'] = df['Place'].astype(str)

import re
df['Place'] = df['Place'].apply(lambda x: re.sub(r'([a-zA-Z])(\()', r'\1 \2', x))
df['Place'] = df['Place'].apply(lambda x: re.sub(r'(\))([a-zA-Z])', r'\1 \2', x))

df['Place'] = df['Place'].apply(lambda x: re.sub(r'([1-9])(\()', r'\1 \2', x))
df['Place'] = df['Place'].apply(lambda x: re.sub(r'(\))([1-9])', r'\1 \2', x))

df['Place'] = df['Place'].apply(lambda x: re.sub(r'([a-zA-Z])([1-9])', r'\1 \2', x))

try:
    df['Sort'] = pd.to_datetime(df['Date'], format="%A %d %B") + pd.offsets.DateOffset(years=121)
    df = df.sort_values(by=["Sort", "Type"], ascending=False)
except:
    pass

df = df[['Date', 'Place', 'Suburb', 'Arrival time', 'Departure time', 'Type']]

df.dropna(inplace=True)

old = pd.read_csv(data_endpoint)

combo = old.append(df)

combo = combo.drop_duplicates(subset=['Date', 'Place', 'Suburb', 'Arrival time', 'Departure time', 'Type'])

with open(data_endpoint, "w") as f:
    combo.to_csv(f, index=False, header=True)