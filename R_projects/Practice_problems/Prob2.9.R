# set working directory and load data 
setwd("/Users/joeburg/Dropbox/Stanford/Stanford_2014-2015/Spring_Quarter/CME_250/Homework/HW1")
data = read.table("Auto.data",header=T,na.strings="?")
predictors = names(data)

# deal with the missing values in the data set - remove cars with 'NA' values
data = na.omit(data)

# find the range, mean, and standard deviation of the quantitative predictors
for(i in 1:7) {
  cat(predictors[i],' range: ',range(data[,i]),'\n')
  cat(predictors[i],' mean: ',mean(data[,i]),'\n')
  cat(predictors[i],' standard deviation: ',sd(data[,i]),'\n\n')
}

# remove the 10th-85th observations and recompute the range, mean, and sd
data_sub = data[-(10:85),]
for(i in 1:7) {
  cat(predictors[i],' range: ',range(data_sub[,i]),'\n')
  cat(predictors[i],' mean: ',mean(data_sub[,i]),'\n')
  cat(predictors[i],' standard deviation: ',sd(data_sub[,i]),'\n\n')
}

# plotting relationships between predictors
plot(data$horsepower, data$mpg)
plot(data$weight, data$mpg)
plot(data$cylinders, data$horsepower)
plot(data$horsepower, data$acceleration)
plot(data$year, data$mpg)
plot(data$displacement, data$mpg)
plot(data$year, data$horsepower)
