# (a) generate data set
set.seed(1)
y=rnorm(100)
x=rnorm(100)
y=x-2*x^2+rnorm(100)

# (b) create scatterplot of x vs y
plot(x,y)

# (c) set random seed and compute the LOOCV errors for models
# (i)Y = β0 + β1X + ε; (ii)Y = β0 + β1X + β2X2 + ε; 
# (iii)Y = β0 +β1X +β2X2 +β3X3 +ε; (iv )Y = β0 +β1X +β2X2 +β3X3 +β4X4 +ε;
library(boot)
Data = data.frame(x, y)
set.seed(1)

cv.error=rep(0,4)
for (i in 1:4){
  glm.fit = glm(y ~ poly(x, i))
  cv.error[i]=cv.glm(Data,glm.fit)$delta[1]
}
cv.error

# (d) set new seed and repeat models in (c)
set.seed(3)
cv.error2=rep(0,4)
for (i in 1:4){
  glm.fit = glm(y ~ poly(x, i))
  cv.error2[i]=cv.glm(Data,glm.fit)$delta[1]
}
cv.error2

