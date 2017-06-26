#读取数据
loandata_borrow <- read.csv('../../output/loandata_borrow_std.csv')
loandata_repay <- read.csv('../../output/loandata_repay_std.csv')
loandata_borrow <- loandata_borrow[,-1]
loandata_repay <- loandata_repay[,-1]
#数据摘要
summary(loandata_borrow)
#查看数据类型
str(loandata_borrow)
#转换数据类型
loandata_borrow$marital_status = as.factor(loandata_borrow$marital_status)
loandata_borrow$house = as.factor(loandata_borrow$house)
loandata_borrow$house_loan = as.factor(loandata_borrow$house_loan)
loandata_borrow$car = as.factor(loandata_borrow$car)
loandata_borrow$car_loan = as.factor(loandata_borrow$car_loan)
loandata_borrow$company_type = as.factor(loandata_borrow$company_type)
loandata_borrow$company_scale = as.factor(loandata_borrow$company_scale)
loandata_borrow$workcity = as.factor(loandata_borrow$workcity)
loandata_borrow$credit_report = as.factor(loandata_borrow$credit_report)
loandata_borrow$identity_authentication = as.factor(loandata_borrow$identity_authentication)
loandata_borrow$job_authentication = as.factor(loandata_borrow$job_authentication)
loandata_borrow$income_authentication = as.factor(loandata_borrow$income_authentication)
loandata_borrow$site_authentication = as.factor(loandata_borrow$site_authentication)
loandata_borrow$topic = as.factor(loandata_borrow$topic)
loandata_borrow$borrow_result = as.factor(loandata_borrow$borrow_result)

loandata_repay$marital_status = as.factor(loandata_repay$marital_status)
loandata_repay$house = as.factor(loandata_repay$house)
loandata_repay$house_loan = as.factor(loandata_repay$house_loan)
loandata_repay$car = as.factor(loandata_repay$car)
loandata_repay$car_loan = as.factor(loandata_repay$car_loan)
loandata_repay$company_type = as.factor(loandata_repay$company_type)
loandata_repay$company_scale = as.factor(loandata_repay$company_scale)
loandata_repay$workcity = as.factor(loandata_repay$workcity)
loandata_repay$credit_report = as.factor(loandata_repay$credit_report)
loandata_repay$identity_authentication = as.factor(loandata_repay$identity_authentication)
loandata_repay$job_authentication = as.factor(loandata_repay$job_authentication)
loandata_repay$income_authentication = as.factor(loandata_repay$income_authentication)
loandata_repay$site_authentication = as.factor(loandata_repay$site_authentication)
loandata_repay$topic = as.factor(loandata_repay$topic)
loandata_repay$repay_result = as.factor(loandata_repay$repay_result)

#对还款数据进行重抽样，平衡不同还款结果之间的比例
table(loandata_repay$repay_result)
loandata_repay_yes <- loandata_repay[loandata_repay$repay_result=='1',]
loandata_repay_no <- loandata_repay[loandata_repay$repay_result=='0',]
num_samples = 410
samples <- sample(nrow(loandata_repay_yes),num_samples)
loandata_repay_new <- rbind(loandata_repay_yes[samples,],loandata_repay_no)


#逻辑回归
lr_borrow <- glm(borrow_result~.,data = loandata_borrow,family = 'binomial')
summary(lr_borrow)

lr_repay <- glm(repay_result~.,data = loandata_repay_new,family = 'binomial')
summary(lr_repay)
