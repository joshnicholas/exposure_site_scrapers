#%%

import pandas as pd 
import requests
import json 

data_endpoint = "data/nsw_exposure_sites.csv"

nsw_json = "https://data.nsw.gov.au/data/dataset/0a52e6c1-bc0b-48af-8b45-d791a6d8e289/resource/f3a28eed-8c2a-437b-8ac1-2dab3cf760f9/download/covid-case-locations-20210701-1000.json"

#%%

## GRAB NSW

r = requests.get(nsw_json)
data = r.text.encode().decode('utf-8-sig')
thing = json.loads(data)
# thing =codecs.decode(r.text, 'utf-8-sig')
nsw = pd.DataFrame(thing['data']['monitor'])

# print(nsw)
# print(nsw.columns)

nsw_count = len(nsw.index)


old = pd.read_csv(data_endpoint)

print(len(old.index))

combo = old.append(nsw)

combo = combo.drop_duplicates(subset=['Venue', 'Address', 'Suburb', 'Date', 'Time'])

with open(data_endpoint, "w") as f:
    combo.to_csv(f, index=False, header=True)



#%%

## GRAB QUEENSLAND

