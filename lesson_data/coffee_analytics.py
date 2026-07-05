import pandas as ps
from matplotlib import pyplot as plt
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO
import uvicorn
path_data='./lesson_data/coffee.csv'
"""
Index(['Country', 'Coffee type', '1990/91', '1991/92', '1992/93', '1993/94',
       '1994/95', '1995/96', '1996/97', '1997/98', '1998/99', '1999/00',
       '2000/01', '2001/02', '2002/03', '2003/04', '2004/05', '2005/06',
       '2006/07', '2007/08', '2008/09', '2009/10', '2010/11', '2011/12',
       '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18',
       '2018/19', '2019/20', 'Total_domestic_consumption'],
      dtype='object')
"""
df=ps.read_csv(path_data)
""" print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.head(10)) """
#SELECT AVG(Total) FROM T GROUP BY Type
results=df.groupby('Coffee type')['Total_domestic_consumption'].agg(['min','max','mean','median'])
""" print(results)
results.plot(kind='bar')
plt.tight_layout()
plt.xticks(rotation=45)
plt.show() """



for c in df.columns:
    is_nan=df[c].isna()
    print(df.loc[is_nan])
#Country where total=0
print(df.loc[df['Total_domestic_consumption']==0])
mean=df['Total_domestic_consumption'].mean()
#Tr replace
df['Total_domestic_consumption'].replace(0,mean,inplace=True)
#TR apply
df['Total_domestic_consumption']=df['Total_domestic_consumption'].apply(lambda v:mean if v==0 else v)
print(df.loc[df['Total_domestic_consumption']==0])
"""
Load vers database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from mysql.connector import connect

import os
DB_USER=os.getenv("DB_USER","postgres")#postgres#root
DB_PASSWORD:str=os.getenv("DB_PASSWORD","pubg4life")
DB_NAME:str=os.getenv("DB_NAME","db_bank")
DB_PORT:str=os.getenv("DB_PORT","5432") #5432 for postgradSQL 3306 for mysql

        ##mysql+mysqlconnector
        ##postgresql+psycopg2
URL:str= 'postgresql+psycopg2://'+DB_USER+':'+DB_PASSWORD+'@localhost:'+DB_PORT+'/'+DB_NAME
connection=create_engine(URL,pool_size=10)
df[['Country','Coffee type','Total_domestic_consumption']].to_sql('T_coffee',con=connection,if_exists='replace',index=False)
app=FastAPI()
@app.get("/dashboard")
def dashboard():
    fig=plt.figure(figsize=(8,4))
    df[['2005/06','2019/20']].plot(kind='line')
    img=BytesIO()
    plt.savefig(img,format='png')
    img.seek(0)
    return StreamingResponse(content=img,media_type='image/png')

if __name__ == '__main__':
    uvicorn.run('coffee_analytics:app',reload=True)