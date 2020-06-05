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



download_file("https://api.covid19india.org/csv/latest/state_wise.csv", r"data/latest_data.csv")
download_file("https://api.covid19india.org/csv/latest/state_wise_daily.csv", r"data/state_daily_raw_data.csv")



with open(r"data/state_district_code.json","r") as f:
    code = json.load(f)
f.close()

df = pd.read_csv(r"data/latest_data.csv")
# df['State'] = df['State_code'].apply(lambda x: code['Statecode'][x])

df.to_csv(r"data/latest_data.csv",index=False)



df = pd.read_csv(r"data/state_daily_raw_data.csv")
melt_cols = list(df.columns)[2:]


new_col = [code["Statecode"][col] for col in melt_cols]
df.columns = list(df.columns)[:2] + new_col
df = pd.melt(df, id_vars = list(df.columns)[:2], value_vars=new_col)
df = df.pivot_table(index=['Date','variable'], columns='Status',
                     values='value', aggfunc='first').reset_index()
df.columns = ["Date","State","NewConfirmed","NewDeceased","NewRecovered"]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date", ascending=True)
df=df.reset_index(drop=True)
df["Confirmed"] = df.groupby(['State'])["NewConfirmed"].cumsum()
df["Deceased"] = df.groupby(['State'])["NewDeceased"].cumsum()
df["Recovered"] = df.groupby(['State'])["NewRecovered"].cumsum()
df["Active"] = df['Confirmed'] - (df['Deceased'] + df['Recovered'])

for i in [2,5,7,10]:
    df['doubling_time_last_'+str(i)+'days'] = np.nan

all_state_df = pd.DataFrame()
state_list = list(set(df.State.values))
for state in state_list:
    df_state = df[df.State == state]
    df_state = df_state.sort_values("Date", ascending=True)
    df_state=df_state.reset_index(drop=True)
    for i in [2,5,7,10]:
        for index in range(i-1,len(df_state)):
    
            df_state['doubling_time_last_'+str(i)+'days'].iat[index] = (np.log(2) * i) / np.log( df_state['Confirmed'].iat[index] / df_state['Confirmed'].iat[index-i+1]  )
            df['doubling_time_last_'+str(i)+'days'] = pd.to_numeric(df['doubling_time_last_'+str(i)+'days'])
            df_state = df_state.replace([np.inf, -np.inf], np.nan)
    
    all_state_df = all_state_df.append(df_state)


all_state_df["Date"] = pd.to_datetime(all_state_df["Date"])
all_state_df = all_state_df.sort_values(["State","Date"], ascending=True)
all_state_df=all_state_df.reset_index(drop=True)

all_state_df.to_csv(r"data/state_daily_data.csv",index=False)

