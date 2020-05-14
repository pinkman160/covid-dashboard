import pandas as pd
import json

df=pd.read_excel('Map data.xlsx',sheet_name = 'Sheet6')
df=df[['Dname' , 'MapName']]
df.set_index('Dname',inplace=True)
dic  = df.to_dict()['MapName']

with open ('district_rename.json','w') as f:
    json.dump(dic,f,indent=4)
f.close()