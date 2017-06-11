library(rpart)
library(Hmisc)
library(Design)

# install.packages("rfimpute")
# library(rfimpute)

# set working directory
setwd("/Users/joeburg/Dropbox/Stanford/Stanford_2014-2015/Spring_Quarter/CME_250/mini_project")

# import data for fitting
dataforFitting = read.csv("dataforFitting.csv", header=TRUE)

# import data to predict
predictThese = read.csv("predictThese.csv", header=TRUE)

# combine data into single data frame (1-70 is training; 71-100 is test)
data = rbind(dataforFitting[,-1], predictThese[,-1])
data = impute(data)
# training = data[1:70,]
# test = data[71,100,]

# impute to deal with missing data
imputedFit = impute(dataforFitting)
imputedPreds = impute(predictThese)

# use CART on data
# cart_tree = rpart(imputed$Age ~ imputed$OwnCar + imputed$Coffee + imputed$CommuteDistance + 
#                     imputed$CommuteTime + imputed$CreditCards + imputed$Credits + imputed$Drinks + 
#                     imputed$OnCampus, imputed, cp = 0)

cart_tree = rpart(Age ~ OwnCar + Coffee + CommuteDistance + CommuteTime + 
                    CreditCards + Credits + Drinks + OnCampus + CommuteMethod + 
                    ErrandsMethod + SocialTime + Weddings + VoiceCalls +
                    Siblings + CashinWallet + Field + Recycle + Countries + HarryPotter, 
                  imputedFit, cp=0)

min_level = which.min(as.vector(cart_tree$cp[,4]))
cart_tree$cp[1:(min_level),]

# summary(cart_tree)
# names(cart_tree)
cart_tree$frame

plotcp(cart_tree)
# plot(cart_tree, branch=0)
# text(cart_tree, pretty = TRUE)
# summary(cart_tree)

preds = predict(cart_tree, imputedPreds)
summary(preds)

# data$OwnCar[71]
# data$OwnCar[100]
# preds[1]

# use cart tree to predict ages
predicted_Ages = matrix(,nrow=30,ncol=2)
for (i in 71:100) {
  if (data$OwnCar[i] == 'Yes') {
    if (data$Credits[i] >= 12.5) {
      age = 20.83
    }
    else {
      if (data$Coffee[i] < 4) {
        age = 22.8
      }
      else {
        age = 24.18
      }
    }
  }
  else {
    if (data$Credits[i] >= 5.5) {
      if (data$CommuteTime[i] < 12.5) {
        age = 24.86
      }
      else {
        age = 27.11
      }
    }
    else {
      age = 28.29
    }
  }
  
  n = i-70
  predicted_Ages[n,1] = n
  predicted_Ages[n,2] = age
}

predicted_Ages
write.csv("predicted_ages.csv",row.names=FALSE)


# # deal with the missing values in the data set - remove cars with 'NA' values
# data = na.omit(data)
# dataforFitting = na.omit(dataforFitting)
# #dataforFitting = impute.knn(dataforFitting, k=5)

# plotting relationships between predictors
#plot(dataforFitting$CommuteDistance, dataforFitting$Age)
#plot(dataforFitting$Credits, dataforFitting$Age)
#plot(dataforFitting$OnCampus, dataforFitting$Age)
#plot(dataforFitting$OwnCar, dataforFitting$Age)
#plot(dataforFitting$PrevResDist, dataforFitting$Age)
#plot(dataforFitting$Field, dataforFitting$Age)
#plot(dataforFitting$SocialTime, dataforFitting$Age)
#plot(dataforFitting$Weddings, dataforFitting$Age)
#plot(dataforFitting$VoiceCalls, dataforFitting$Age)
#plot(dataforFitting$Smartphones, dataforFitting$Age)
#plot(dataforFitting$Coffee, dataforFitting$Age)
#plot(dataforFitting$Siblings, dataforFitting$Age)
#plot(dataforFitting$LongestFlight, dataforFitting$Age)
#plot(dataforFitting$SportsHours, dataforFitting$Age)
#plot(dataforFitting$HarryPotter, dataforFitting$Age)
#plot(dataforFitting$Drinks, dataforFitting$Age)
#plot(dataforFitting$CashinWallet, dataforFitting$Age)
#plot(dataforFitting$CreditCards, dataforFitting$Age)
