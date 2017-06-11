# set working directory and load data 
setwd("/Users/joeburg/Dropbox/Stanford/Stanford_2014-2015/Spring_Quarter/CME_250/Homework/HW1")
data = read.table("Auto.data",header=T,na.strings="?")
predictors = names(data)

# deal with the missing values in the data set - remove cars with 'NA' values
data = na.omit(data)

# scatter plot matrix with all the variables
pairs(data)

# compute the matrix of correlations (exlcude name variable)
data_sub = subset(data,select=-name)
cor(data_sub)

# perform multiple linear regression with mpg as the response and all other vars as predictors
model = lm(mpg ~ ., data=data_sub)
summary(model)

# use * and : symbols to fit linear regression models with interaction effects
# note: Y ~ A*B -> Y = c0 + c1A + c2B + c3AB
# Y ~ A:B -> Y = c0 + c1AB
# so Y ~ A*B is equivalent to Y ~ A + B + A:B
# we will just use * since it contains :
model2 = lm(mpg ~ weight*acceleration + weight*horsepower, data=data_sub)
summary(model2)

model3 = lm(mpg ~ weight*displacement + cylinders*displacement, data=data_sub)
summary(model3)

# models with transformations like log(X), sqrt(X), X^2
model4 = lm(mpg ~ I(acceleration)^2 + log(displacement) + sqrt(weight) + sqrt(horsepower), data=data_sub)
summary(model4)

model5 = lm(mpg ~ log(weight) + log(displacement) + sqrt(horsepower), data=data_sub)
summary(model5)