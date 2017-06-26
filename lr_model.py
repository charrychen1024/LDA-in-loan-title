from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

#读取原始贷款数据
loandata = pd.read_csv('./data/loandata_clean.csv')
#读取主题数据
topic = pd.read_table('./output/doc_topic_one.txt',sep='\n')
#添加主题列
loandata['topic'] = topic
#将借款结果做0-1分类
loandata['borrow_result'] = list(map(lambda x: 0 if x==0 else 1,loandata.loan_status))
#将还款结果做0-1分类
loandata['repay_result'] = list(map(lambda x: 0 if x==3 else (1 if x==2 else np.nan),loandata.loan_status))
#复制新数据
loandata_borrow = loandata.copy()
loandata_borrow.drop(['webpage','loan_title','loan_description','loan_status','repay_result'],axis=1,inplace=True)
loandata_repay = loandata.copy()
loandata_repay.drop(['webpage','loan_title','loan_description','loan_status','borrow_result'],axis=1,inplace=True)
#删除loandata_repay中借款失败的数据
loandata_repay.dropna(inplace=True)

#数据标准化
columns_scale = ['loan_amount','avaiable_amount','total_loan_amount','need_to_payoff','overdue_amount']
std = StandardScaler().fit_transform(loandata_borrow.loc[:,columns_scale])
loandata_borrow.drop(columns_scale,axis=1,inplace=True)
loandata_borrow_std = loandata_borrow.join(pd.DataFrame(std,columns=columns_scale))
std = StandardScaler().fit_transform(loandata_repay.loc[:,columns_scale])
loandata_repay.drop(columns_scale,axis=1,inplace=True)
loandata_repay_std = loandata_repay.join(pd.DataFrame(std,columns=columns_scale))
#将数据写入文件
loandata_borrow_std.to_csv(path_or_buf='./output/loandata_borrow_std.csv')
loandata_repay_std.to_csv(path_or_buf='./output/loandata_repay_std.csv')

#哑变量编码
def dummy_variable_encode(dataframe,column_name):
    dummy_variable = pd.get_dummies(dataframe[column_name],prefix=column_name,drop_first=True)
    dataframe_new = dataframe.join(dummy_variable)
    del dataframe_new[column_name]
    return dataframe_new

#loandata_borrow = dummy_variable_encode(loandata_borrow,'credit_score')
#loandata_borrow = dummy_variable_encode(loandata_borrow,'age')
#loandata_borrow = dummy_variable_encode(loandata_borrow,'education')
loandata_borrow = dummy_variable_encode(loandata_borrow,'marital_status')
#loandata_borrow = dummy_variable_encode(loandata_borrow,'income')
loandata_borrow = dummy_variable_encode(loandata_borrow,'house')
loandata_borrow = dummy_variable_encode(loandata_borrow,'house_loan')
loandata_borrow = dummy_variable_encode(loandata_borrow,'car')
loandata_borrow = dummy_variable_encode(loandata_borrow,'car_loan')
loandata_borrow = dummy_variable_encode(loandata_borrow,'company_type')
loandata_borrow = dummy_variable_encode(loandata_borrow,'company_scale')
loandata_borrow = dummy_variable_encode(loandata_borrow,'workcity')
#loandata_borrow = dummy_variable_encode(loandata_borrow,'work_duration')
loandata_borrow = dummy_variable_encode(loandata_borrow,'credit_report')
loandata_borrow = dummy_variable_encode(loandata_borrow,'identity_authentication')
loandata_borrow = dummy_variable_encode(loandata_borrow,'job_authentication')
loandata_borrow = dummy_variable_encode(loandata_borrow,'income_authentication')
loandata_borrow = dummy_variable_encode(loandata_borrow,'site_authentication')
loandata_borrow = dummy_variable_encode(loandata_borrow,'topic')

#loandata_repay = dummy_variable_encode(loandata_repay,'credit_score')
#loandata_repay = dummy_variable_encode(loandata_repay,'age')
#loandata_repay = dummy_variable_encode(loandata_repay,'education')
loandata_repay = dummy_variable_encode(loandata_repay,'marital_status')
#loandata_repay = dummy_variable_encode(loandata_repay,'income')
loandata_repay = dummy_variable_encode(loandata_repay,'house')
loandata_repay = dummy_variable_encode(loandata_repay,'house_loan')
loandata_repay = dummy_variable_encode(loandata_repay,'car')
loandata_repay = dummy_variable_encode(loandata_repay,'car_loan')
loandata_repay = dummy_variable_encode(loandata_repay,'company_type')
loandata_repay = dummy_variable_encode(loandata_repay,'company_scale')
loandata_repay = dummy_variable_encode(loandata_repay,'workcity')
#loandata_repay = dummy_variable_encode(loandata_repay,'work_duration')
loandata_repay = dummy_variable_encode(loandata_repay,'credit_report')
loandata_repay = dummy_variable_encode(loandata_repay,'identity_authentication')
loandata_repay = dummy_variable_encode(loandata_repay,'job_authentication')
loandata_repay = dummy_variable_encode(loandata_repay,'income_authentication')
loandata_repay = dummy_variable_encode(loandata_repay,'site_authentication')
loandata_repay = dummy_variable_encode(loandata_repay,'topic')

#逻辑回归-机器学习模块
X = loandata_borrow_std.drop(['borrow_result'],axis=1)
y = loandata_borrow_std['borrow_result']
lr = LogisticRegression()
lr_title = lr.fit_transform(X,y)
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

print(classification_report(y,lr.predict(X)))
print(confusion_matrix(y,lr.predict(X)))
#逻辑回归-统计模块
import statsmodels.api as sm

X = loandata_borrow_std.drop(['borrow_result'],axis=1)
y = loandata_borrow_std['borrow_result']
X = sm.add_constant(X)
logit_mod = sm.Logit(y,X)
logit_res = logit_mod.fit(maxiter=100)
print(logit_res.summary())
