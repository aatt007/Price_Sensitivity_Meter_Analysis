import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('psm.csv')
print(df)
#print(df.columns)
#print(df.info())
#print(df.describe())

df=df.unstack().reset_index()
print(df)
df=df.groupby(['level_0',0]).count().reset_index()
df=df.rename(columns={'level_0': 'type',0: 'price', 'level_1':'count'})
df['sum']=df.groupby(['type'])['count'].transform('sum')
df['cumsum']=df.groupby(['type'])['count'].cumsum()
df['percent']=df['cumsum']/df['sum']*100
df=df.pivot_table('percent', 'price','type' )
#df=df.ffill().fillna(0)
df=df.interpolate().fillna(0)
df['Too Cheap']=100-df['Too Cheap']
df['Cheap']=100-df['Cheap']
df.plot()
plt.show()
#print(df)
