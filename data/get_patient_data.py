import requests,json,os
import pandas as pd

data = []

for i in range(1,4):
    r = requests.get('https://api.covid19india.org/raw_data' + str(i) + '.json')
    with open("patient_raw_data" + str(i) + ".json","w") as f:
        json.dump (r.json() ,f, indent=4 )
    f.close()
    data.extend(r.json()["raw_data"])

df = pd.DataFrame(data = data)
df.to_csv("patient_raw_data.csv",index=False)
