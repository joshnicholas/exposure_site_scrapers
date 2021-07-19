import requests
import pandas as pd 


data_endpoint = "data/vic_exposure_sites.csv"

file_name = 'vic-hotspot_download.csv'

ceevee = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSNouXrJ8UQ-tn6bAxzrOdLINuoOtn01fSjooql0O3XQlj4_ldFiglzOmDm--t2jy1k-ABK6LMzPScs/pub?gid=1075463302&single=true&output=csv'

df = pd.read_csv(ceevee)

df['Added_date_dtm'] = pd.to_datetime(df['Added_date_dtm'])

df = df.sort_values(by='Added_date_dtm', ascending=False)

df = df[['Suburb', 'Site_title','Exposure_date', 'Exposure_time',
       'Notes', 'Added_date', 'Advice_instruction' ]]

df.columns = ['Suburb', 'Site', 'Exposure day', 'Exposure time', 'Notes', 'Date added', 'Health advice']

# print(df)

old = pd.read_csv(data_endpoint)

combo = old.append(df)

combo = combo.drop_duplicates(subset=['Suburb', 'Site', 'Exposure day', 'Exposure time', 'Notes', 'Date added', 'Health advice'])

with open(data_endpoint, "w") as f:
    combo.to_csv(f, index=False, header=True)