import pandas as pd
from pandas.core.frame import DataFrame
import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Series, DataFrame
# 0'企业名称' 
# 1'经营状态' 
# 2'法定代表人' 
# 3'注册资本' 
# 4'成立日期' 
# 5'所属省份' 
# 6'所属城市' 
# 7'电话' 
# 8'更多电话' 
# 9'邮箱'
# 10'统一社会信用代码' 
# 11'纳税人识别号' 
# 12'注册号' 
# 13'组织机构代码' 
# 14'参保人數' 
# 15'企业类型' 
# 16'所属行业' 
# 17'网址' 
# 18'企业地址'
# 19'经营范围'



if __name__ == "__main__":
    path = 'D:\\123456789.xls'
    jjj=pd.read_excel(path)
#
#    state = jjj.groupby(keys='经营状态')
#    #获取所有状态
#    for i in range(len(jjj)):
#        data = jjj.loc[i].values
#        if data[1] == "在业" :
#            print("\n{0}".format(data[0:2]))       
#    print("\n{0}".format(jjj.columns.values))

    jjj.groupby("经营状态").
#print("\n{0}".format(jjj.columns.values))

#dir(state)
#jjj.dtypes
#jjj.values
