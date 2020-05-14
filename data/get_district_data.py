import requests,json,os
import pandas as pd

r = requests.get('https://api.covid19india.org/districts_daily.json')

with open("district_daily_data.json","w") as f:
    json.dump (r.json() ,f, indent=4 )
f.close()

df=pd.DataFrame()
data=r.json()
for state in data['districtsDaily']:
    for district in data['districtsDaily'][state]:
        district_df = pd.DataFrame(data = data['districtsDaily'][state][district])
        district_df['District'] = district
        district_df['State'] = state
        df = df.append(district_df)
df = df[["State","District","date","confirmed","active","recovered","deceased"]]
df.columns = ["State","District","Date","Confirmed","Active","Recovered","Deceased"]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date", ascending=True)
df=df.reset_index(drop=True)
df["NewConfirmed"] =  df.groupby(['District'])["Confirmed"].diff().fillna(0)
df["NewDeceased"] = df.groupby(['District'])["Deceased"].diff().fillna(0)
df["NewRecovered"] = df.groupby(['District'])["Recovered"].diff().fillna(0)



with open ('district_rename.json','r') as f:
    district_dic = json.load(f)
f.close()

def district_rename(district):
    if district in district_dic.keys():
        return(district_dic[district])
    else:
        return(district)

df['NewDistrict'] = df['District'].apply(lambda x: district_rename(x))


df.loc[df.District == 'Dadra and Nagar Haveli' , 'State'] = 'Dadra and Nagar Haveli'
# df.loc[df.District  'Daman' , 'State'] = 'Daman and Diu'
# df.loc[df.District  'Diu' , 'State'] = 'Daman and Diu' 

df.to_csv("district_daily_data.csv", index = False)