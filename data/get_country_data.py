import requests,json,os,csv
import pandas as pd
import numpy as np


def download_file(url, filename):
    ''' Downloads file from the url and save it as filename '''
    print('Downloading File')
    response = requests.get(url)
    # Check if the response is ok (200)
    if response.status_code == 200:
        # Open file and write the content
        with open(filename, 'wb') as file:
            # A chunk of 128 bytes
            for chunk in response:
                file.write(chunk)


download_file("https://api.covid19india.org/csv/latest/case_time_series.csv", "country_daily_data.csv")

df = pd.read_csv("country_daily_data.csv")
df.columns = ['Date', 'NewConfirmed', 'Confirmed', 'NewRecovered','Recovered', 'NewDeceased', 'Deceased']
df["Active"] = df['Confirmed'] - (df['Deceased'] + df['Recovered'])
df['Date'] = df['Date'].apply(lambda x: x +" 2020")
df['Date'] = pd.to_datetime(df['Date'])

for i in [2,5,7,10]:
    df['doubling_time_last_'+str(i)+'days'] = np.nan
    for index in range(i-1,len(df)):
        df['doubling_time_last_'+str(i)+'days'].iat[index] = (np.log(2) * i) / np.log( df['Confirmed'].iat[index] / df['Confirmed'].iat[index-i+1]  )
        df['doubling_time_last_'+str(i)+'days'] = pd.to_numeric(df['doubling_time_last_'+str(i)+'days'])
        df = df.replace([np.inf, -np.inf], np.nan)

df["State"] = "India"

all_state_df = pd.read_csv("state_daily_data.csv")
all_state_df['Date'] = pd.to_datetime(all_state_df['Date'])


all_state_df = all_state_df[all_state_df["State"]!="India"]
df = df.append(all_state_df)


df.to_csv("country_daily_data.csv",index=False)

# print(df['doubling time'])