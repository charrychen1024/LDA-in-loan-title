library(RODBC)

#从mysql中读取数据
conn <- odbcConnect('mysqlodbc','root','charrychen')
loandata_all <- sqlFetch(conn,'loandata_clean')
close(conn)
as.data.frame(loandata_all)

#删除无用列
loandata_all <- loandata_all[,-c(1,2,3)]

#转换数据类型
loandata_all$loan_status <- as.factor(loandata_all$loan_status)
loandata_all$marital_status <- as.factor(loandata_all$marital_status)
loandata_all$house <- as.factor(loandata_all$house)
loandata_all$house_loan <- as.factor(loandata_all$house_loan)
loandata_all$car <- as.factor(loandata_all$car)
loandata_all$car_loan <- as.factor(loandata_all$car_loan)
loandata_all$company_scale <- as.factor(loandata_all$company_scale)
loandata_all$company_type <- as.factor(loandata_all$company_type)
loandata_all$workcity <- as.factor(loandata_all$workcity)
loandata_all$credit_report <- as.factor(loandata_all$credit_report)
loandata_all$identity_authentication <- as.factor(loandata_all$identity_authentication)
loandata_all$job_authentication <- as.factor(loandata_all$job_authentication)
loandata_all$income_authentication <- as.factor(loandata_all$income_authentication)
loandata_all$site_authentication <- as.factor(loandata_all$site_authentication)

#按借款和还款状态分类
loandata_all_borrow <- loandata_all
loandata_all_repay <- loandata_all

loandata_all_borrow$borrow_result <- ifelse(loandata_all$loan_status=='0',0,1)
loandata_all_repay$repay_result <- ifelse(loandata_all$loan_status=='3',0,ifelse(loandata_all$loan_status=='2',1,NA))

loandata_all_borrow$borrow_result <- as.factor(loandata_all_borrow$borrow_result)
loandata_all_repay$repay_result <- as.factor(loandata_all_repay$repay_result)
loandata_all_borrow <- loandata_all_borrow[,-4]
loandata_all_repay <- loandata_all_repay[,-4]

loandata_all_repay <- na.omit(loandata_all_repay) #删除缺失值

#数据标准化


#抽样
loandata_all_repay_yes <- loandata_all_repay[loandata_all_repay$repay_result=='1',]
loandata_all_repay_no <- loandata_all_repay[loandata_all_repay$repay_result=='0',]

num_samples <- 156
samples <- sample(nrow(loandata_all_repay_yes),num_samples)
loandata_repay_new <- rbind(loandata_all_repay_no,loandata_all_repay_yes[samples,])

#逻辑回归
lr_borrow <- glm(borrow_result~.,data = loandata_borrow,family = 'binomial')
summary(lr_borrow)

lr_repay <- glm(repay_result~.,data = loandata_repay_new,family = 'binomial')
summary(lr_repay)