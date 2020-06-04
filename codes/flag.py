import shutil
import os
import pandas as pd

df = pd.read_csv('flag_map.csv')

for index,row in df.iterrows():
    src_file = r'png/'+str(row[1])
    dst_file = r'flag_icons/'+str(row[2]).replace('"',"") 
    shutil.copy(src_file,dst_file)