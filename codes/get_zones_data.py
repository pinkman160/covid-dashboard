import requests,json,os
import pandas as pd

r = requests.get('https://api.covid19india.org/zones.json')

with open("district_zones_data.json","w") as f:
    json.dump (r.json() ,f, indent=4 )
f.close()

data = r.json()
df = pd.DataFrame(data = data['zones'])
df = df [['state','statecode','district', 'districtcode', 'lastupdated', 'source',  'zone']]
df.columns = ['State','Statecode','District', 'Districtcode', 'lastupdated', 'Source',  'Zone']
df.loc[df['District'] == 'Dadra and Nagar Haveli' , 'State'] = 'Dadra and Nagar Haveli'
df.loc[df['District'] == 'Dadra and Nagar Haveli' , 'Statecode'] = 'DD'
df.loc[df['District'] == 'Dadra and Nagar Haveli' , 'Districtcode'] = 'DN_Dadra and Nagar Haveli'

df.loc[df['District'] == 'Daman' , 'State'] = 'Daman and Diu'
df.loc[df['District'] == 'Diu' , 'State'] = 'Daman and Diu'

state_codes_df = df[['Statecode','State']].drop_duplicates()
district_codes_df = df[['Districtcode', 'District']].drop_duplicates()
codes = dict.fromkeys(["Statecode" ,"Districtcode"])
codes["Statecode"] = dict(zip(state_codes_df.Statecode,state_codes_df.State))
codes["Districtcode"] = dict(zip(district_codes_df.Districtcode,district_codes_df.District))
codes["Statecode"]["DN"] = "Dadra and Nagar Haveli"
codes["Statecode"]["DD"] = "Daman and Diu"
codes["Statecode"]["TT"] = "India"

with open("state_district_code.json","w") as f:
    json.dump (codes ,f, indent=4 )
f.close()

# df.loc[df['District'] == 'Daman' , 'Statecode'] = 'DN'
# df.loc[df['District'] == 'Dadra and Nagar Haveli' , 'Districtcode'] = 'DN_Dadra and Nagar Haveli'

with open ('district_rename.json','r') as f:
    district_dic = json.load(f)
f.close()

def district_rename(district):
    if district in district_dic.keys():
        return(district_dic[district])
    else:
        return(district)

df['NewDistrict'] = df['District'].apply(lambda x: district_rename(x))

df.to_csv("district_zones_data.csv", index = False)

