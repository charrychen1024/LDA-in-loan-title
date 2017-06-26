import pymysql
import pandas as pd
import numpy as np

#从mysql中读取所有借款数据
conn = pymysql.connect(host='127.0.0.1',user='root',password='charrychen',database='renrendai',charset='utf8')
loandata = pd.read_sql(sql='SELECT * FROM loandata_clean',con=conn)
conn.close()

#转换数据类型
loandata.loan_status = loandata.loan_status.astype(np.int8)
loandata.credit_score = loandata.credit_score.astype(np.int8)
loandata.age = loandata.age.astype(np.int8)
loandata.education = loandata.education.astype(np.int8)
loandata.marital_status = loandata.marital_status.astype(np.int8)
loandata.income = loandata.income.astype(np.int8)
loandata.house = loandata.house.astype(np.int8)
loandata.house_loan = loandata.house_loan.astype(np.int8)
loandata.car = loandata.car.astype(np.int8)
loandata.car_loan = loandata.car_loan.astype(np.int8)
loandata.company_type = loandata.company_type.astype(np.int8)
loandata.company_scale = loandata.company_scale.astype(np.int8)
loandata.workcity = loandata.workcity.astype(np.int8)
loandata.work_duration = loandata.work_duration.astype(np.int8)
loandata.credit_report = loandata.credit_report.astype(np.int8)
loandata.identity_authentication = loandata.identity_authentication.astype(np.int8)
loandata.job_authentication = loandata.job_authentication.astype(np.int8)
loandata.income_authentication = loandata.income_authentication.astype(np.int8)
loandata.site_authentication = loandata.site_authentication.astype(np.int8)

#将借款结果和还款结果分类
loandata['borrow_result'] = list(map(lambda x: 0 if x==0 else 1,loandata['loan_status']))
loandata['repay_result'] = list(map(lambda x: 0 if x==3 else (1 if x==2 else np.nan), loandata['loan_status']))

#区分借款数据集和还款数据集
loandata_borrow = loandata.copy()
loandata_borrow.drop(['loan_status','repay_result'],axis=1,inplace=True)
loandata_repay = loandata.copy()
loandata_repay.drop(['loan_status','borrow_result'],axis=1,inplace=True)
loandata_repay.dropna(inplace=True)
#描述性统计
loandata.describe()

#获取单列不同类别出现次数
def get_group(data_series):
    return data_series.groupby(data_series).count()

#可视化分析
import matplotlib.pyplot as plt

#连续型变量
plt.subplot(1,3,1)
plt.hist(loandata['loan_amount']) #借款数量分布
plt.ylabel('Number of samples')
plt.xlabel('Loan amount')
plt.subplot(1,3,2)
plt.hist(loandata['interest_rate']) #借款年利率分布
plt.ylabel('Number of samples')
plt.xlabel('Interest rate')
plt.subplot(1,3,3)
plt.hist(loandata['repayment_period']) #还款周期分布
plt.ylabel('Number of samples')
plt.xlabel('Repayment period')
#plt.savefig('./output/continuous variables.png')
plt.show()
#离散型变量
#信用分分布
plt.subplot(4,2,1)
group = get_group(loandata.credit_score)
labels = ['0-99','100-109','110-129','130-149','150-179','180-209','>=209']
plt.pie(x=group.values,labels=labels)
plt.xlabel('Credit score')
#借款状态分布
plt.subplot(4,2,2)
group = get_group(loandata.loan_status)
plt.pie(x=group.values,labels=['failed','repaying','closed','bad debt'])
plt.xlabel('Loan status')
#年龄分布
plt.subplot(4,2,3)
group = get_group(loandata.age)
plt.bar(left=group.index,height=group.values)
plt.ylabel('Number of samples')
plt.xlabel('Age')
plt.xticks(group.index,['18-25','26-35','36-45','46-55','56-65','>65'])
#受教育程度分布
plt.subplot(4,2,4)
group = get_group(loandata.education)
plt.bar(left=group.index,height=group.values)
plt.ylabel('Number of samples')
plt.xlabel('Education')
plt.xticks(group.index,['null','highschool or below','junior college','undergraduate','post graduate'])
#婚姻状态分布
plt.subplot(4,2,5)
group = get_group(loandata.marital_status)
plt.bar(left=group.index,height=group.values)
plt.ylabel('Number of samples')
plt.xlabel('Marital')
plt.xticks(group.index,['null','single','married','divorce','widowed'])
#收入情况分布
plt.subplot(4,2,6)
group = get_group(loandata.income)
plt.bar(left=group.index,height=group.values)
plt.ylabel('Number of samples')
plt.xlabel('Income')
plt.xticks(group.index,['null','<1000','1000-2000','2000-5000','5000-10000','10000-20000','20000-50000','>50000'])
#房产，房贷，车产，车贷分布
plt.subplot(4,2,7)
group1 = get_group(loandata.house)
group2 = get_group(loandata.house_loan)
group3 = get_group(loandata.car)
group4 = get_group(loandata.car_loan)
series1 = []
series1.append(group1.values[0])
series1.append(group2.values[0])
series1.append(group3.values[0])
series1.append(group4.values[0])
series2 = []
series2.append(group1.values[1])
series2.append(group2.values[1])
series2.append(group3.values[1])
series2.append(group4.values[1])
index = range(4)
ticks = ['house','house_loan','car','car_loan']
plt.bar(index,series1,label='no')
plt.bar(index,series2,bottom=series1,label='yes')
plt.xticks(index,ticks)
plt.ylabel('Number of samples')
plt.xlabel('House and Car')
plt.legend(loc='upperright')
#认证情况分布
plt.subplot(4,2,8)
group1 = get_group(loandata.identity_authentication)
group2 = get_group(loandata.job_authentication)
group3 = get_group(loandata.income_authentication)
group4 = get_group(loandata.site_authentication)
series1 = []
series1.append(group1.values[0])
series1.append(group2.values[0])
series1.append(group3.values[0])
series1.append(group4.values[0])
series2 = []
series2.append(group1.values[1])
series2.append(group2.values[1])
series2.append(group3.values[1])
series2.append(group4.values[1])
index = range(4)
ticks = ['indentity','job','income','site']
plt.xticks(index,ticks)
plt.bar(index,series1,label='no')
plt.bar(index,series2,bottom=series1,label='yes')
plt.ylabel('Number of samples')
plt.xlabel('Authentication')
plt.legend(loc='upperright')
#plt.savefig('./output/discrete variables.png')
plt.show()
