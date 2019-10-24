# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:46:47 2019

@author: h
"""

import pandas as pd
from pandas import DataFrame 


df=pd.read_excel('d:/testone/qichacha/zaici.xlsx')
##选取公司非空和注册资本非空的数据，918条只剩下700条记录

df2=df[df['公司'].notna() & df['注册资本'].notna()& df['注册资本'].str.contains('^\d.*')]

##分列处理

res=df2['注册资本'].str.split('万',expand=True)
res
df2[['数字','货币']]=res

##文本转数字

df2['数字2'] = df2['数字'].astype('float')


###限定大于1000万人民币和所有非人民币单位的公司，剩下400多条记录

cond=("数字2>=100 and 货币=='元人民币'" ) 

df3=df2.query(cond) 

cond1=("货币!='元人民币'" )

df3=df3.append(df2.query(cond1) )


#增加成立时间
df4=df3
df4['年数']=2019-(df4['成立时间'].str.split('-').str[0].astype("int"))

#再次筛去那些状态为销的公司，还有公司抬头为空的公司
df4=df4[-df4['状态'].str.contains('销')]
df4=df4[-df4['公司抬头'].isnull()]   #正常在的公司，公司抬头不得为空

#重新排序

df5=df4.sort_values(by=['所属行业','货币','数字2','年数',"公司"],ascending= False)  

#导出
df5.to_excel('df5.xlsx')



#指定替换数值
#for index,row in df5.iterrows():
#    if row['备注']==1:
#        sss=row['序号']
#        df1.备注[df1['序号']==sss]='1'