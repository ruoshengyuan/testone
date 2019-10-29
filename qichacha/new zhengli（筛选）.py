# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:56:27 2019

@author: h
"""

import pandas as pd
from pandas import DataFrame 
df=pd.read_excel('d:/testone/qichacha/zaici.xlsx')
df['备注']=''
df.备注[df['公司抬头'].isna()]='公司抬头为空'
df[df.备注=='公司抬头为空']
df.备注[df['注册资本'].isna()|df['注册资本'].str.contains('-')]='注册资本异常'
df.备注[df['状态'].str.contains('销')|df['状态'].isna()]='状态异常'

res=df['注册资本'].str.split('万',expand=True)
df[['数字','货币']]=res

df['数字2']=df[df['数字'].str.contains('^\d.*\d$')&df['数字'].notna()]['数字'].astype('float')



df.备注[(df['数字2'].notna())&(df['数字2']<=100)&(df['货币']=='元人民币')]='注册资本小于100万'

df.to_excel('df.xlsx')


"数字2<=100 & 货币=='元人民币'"



df['数字'].str.contains('^\d.*\d$')&df['数字'].notna()]

df['数字2']<=100&df['数字2'].notna()&df['货币']=='元人民币'&df['货币'].notna()