import pandas as pd

import numpy as np


df=pd.read_csv('attribution data.csv')
df=df.head(10000)
print(df.columns)
print(df.info())
print(df.describe())
print(df['channel'].unique())

df=df.sort_values(['cookie', 'time'], ascending=[False, True])
df['journey_pos']=df.groupby('cookie').cumcount() + 1
#print(df[['cookie', 'time','journey_pos']])

df_paths=df.groupby('cookie')['channel'].aggregate(lambda x: x.unique().tolist()).reset_index()
df_last_interaction=df.drop_duplicates('cookie', keep='last')[['cookie', 'conversion']]
df_paths=pd.merge(df_paths, df_last_interaction, how='left', on='cookie')
df_paths['path']=pd.NA
for x, row in df_paths.iterrows():
    path=['Start']
    if row['conversion']==0:
        path.append(row['channel'] +['Null'])
    else:
        path.append(row['channel'] +['Converted'])
    df_paths.at[x, 'path']= path

print(df_paths[['cookie', 'channel', 'path']])

list_of_paths=df_paths['path']
total_convert=df['conversion'].sum()
baseconv_rate=total_convert/len(list_of_paths)
print(total_convert, baseconv_rate)