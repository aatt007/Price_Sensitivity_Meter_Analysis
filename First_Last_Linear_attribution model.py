import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_excel('channel_attribution.xlsx')
print(df)
print(df.dtypes)


cols=df.columns
for col in cols:
    df[col]=df[col].astype(str)
    df[col]=df[col].map(lambda x: str(x)[:-2] if '.'in x else str(x))
    #print(df[col])


df['Path']=''
for i in df.index:
    for x in cols:
        df.at[i, 'Path']=df.at[i, 'Path'] + df.at[i, x] + '>'
        #print(df['Path'])

df['Path']=df['Path'].map(lambda x:x.split('>21')[0])
#print(df['Path'])

df['Conversion']=1
df=df[['Path', 'Conversion']]
#print(df)
df=df.groupby('Path').sum().reset_index()
#print(df)
#df.to_excel('path.xlsx', index=False)

df['first touch']=df['Path'].apply(lambda x: x.split('>')[0])
#print(df['first touch'])
df_ft=pd.DataFrame()
df_ft['channel']=df['first touch']
df_ft['attribution']='first touch'
df_ft['Conversion']= 1
df_ft=df_ft.groupby(['channel', 'attribution']).sum().reset_index()
#print(df_ft)

df['last touch']=df['Path'].apply(lambda x: x.split('>')[-1])
df_lt=pd.DataFrame()
df_lt['channel']=df['last touch']
df_lt['attribution']='last touch'
df_lt['Conversion']=1
df_lt=df_lt.groupby(['channel', 'attribution']).sum().reset_index()
#print(df_lt)

channel=[]
conversion=[]
for i in df.index:
    for j in df.at[i, 'Path'].split('>'):
        channel.append(j)
        conversion.append(1/len(df.at[i,'Path'].split('>')))
df_linear=pd.DataFrame()
df_linear['channel']=channel
df_linear['attribution']='linear'
df_linear['Conversion']= conversion
df_linear=df_linear.groupby(['channel', 'attribution']).sum().reset_index()
#print(df_linear)

df_total=pd.concat([df_ft, df_lt, df_linear])
df_total['channel']=df_total['channel'].astype(int)
df_total.sort_values(by='channel', ascending=True, inplace=True)
print(df_total)

sns.barplot(x='channel', y='Conversion', hue='attribution',data=df_total)

plt.show()