import requests,json,os
import pandas as pd
import numpy as np

r = requests.get('https://corona.lmao.ninja/v2/historical?lastdays=150')

with open("world_daily_data.json","w") as f:
    json.dump (r.json() ,f, indent=4 )
f.close()
raw_data=r.json()

# print(raw_data[0]['timeline'][].items())
all_df = pd.DataFrame()
for data in raw_data:
    c_data = []
    for case,values in data['timeline'].items():
        for value in values.items():
            value = list(value)
            value.append(case)
            c_data.append(value)
    df=pd.DataFrame(c_data,columns = ['Date','Count','Case_type']) 
    
    df['Province'] = np.nan
    df['Country'] = data['country']  
    if not data['province']:
        df['Province'] = data['country']
    else:
        df['Province'] = data['province']
    all_df = all_df.append(df)

all_df = pd.pivot_table(all_df,index = ['Country','Province','Date'],columns = ['Case_type'], values = ['Count']).reset_index()
all_df.columns = ['Country','Province','Date','Confirmed','Deceased','Recovered']
all_df["Active"] = all_df['Confirmed'] - (all_df['Deceased'] + all_df['Recovered'])
all_df['Date'] = pd.to_datetime(all_df['Date'])
all_df['Province'] = all_df['Province'].apply(lambda x: str(x).capitalize())
all_df = all_df.sort_values(['Country','Province','Date'], ascending=True)

cols = list(all_df.columns)[3:]

all_df = all_df.groupby(['Country','Date'])[cols].sum().fillna(0).reset_index()
all_df.drop_duplicates(inplace = True)
all_df = all_df[['Country','Date']+cols]
all_df = all_df.sort_values(['Country','Date'], ascending=True)

all_df=all_df[all_df['Confirmed']>0]
all_df = all_df.sort_values(['Country','Date'], ascending=True).reset_index()

# grouped_df = all_df.groupby(['Date'])[cols].sum().fillna(0).reset_index()
# grouped_df['Country'] = 'Worldwide'
# grouped_df = grouped_df[['Country','Date']+cols]

# all_df = all_df.append(grouped_df)
# all_df = all_df.reset_index()
all_df['Day'] = all_df.groupby('Country')['Date'].transform(lambda x: (x - x.iat[0]).dt.days).reset_index()['Date']

# all_df["NewConfirmed"] =  all_df.groupby(['Country','Province'])["Confirmed"].diff().fillna(0)
# all_df["NewDeceased"] = all_df.groupby(['Country','Province'])["Deceased"].diff().fillna(0)
# all_df["NewRecovered"] = all_df.groupby(['Country','Province'])["Recovered"].diff().fillna(0)

for i in [2,5,7,10]:
    all_df['doubling_time_last_'+str(i)+'days'] = np.nan

all_countries_df = pd.DataFrame()
con_list = list(set(all_df.Country.values))
for con in con_list:
    df_con = all_df[all_df.Country == con]
    df_con = df_con.sort_values("Date", ascending=True)
    df_con=df_con.reset_index(drop=True)
    for i in [2,5,7,10]:
        for index in range(i-1,len(df_con)):
    # 
            df_con['doubling_time_last_'+str(i)+'days'].iat[index] = (np.log(2) * i) / np.log( df_con['Confirmed'].iat[index] / df_con['Confirmed'].iat[index-i+1]  )
            df_con['doubling_time_last_'+str(i)+'days'] = pd.to_numeric(df_con['doubling_time_last_'+str(i)+'days'])
            df_con = df_con.replace([np.inf, -np.inf], np.nan)

    all_countries_df = all_countries_df.append(df_con)


all_countries_df = all_countries_df.sort_values(['Country','Date'], ascending=True).reset_index()


all_countries_df.to_csv('world_daily_data.csv',index=False)

# 