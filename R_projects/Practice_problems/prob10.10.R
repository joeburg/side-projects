# (a) generate x set
set.seed(3)
x = matrix(rnorm(20*3*50,mean=0,sd=0.5),ncol=50)
x[1:20,2] = -3
x[21:40,1] = 3
x[21:40,2] = 3
x[41:60,1] = -3

# (b) perform PCA 
pr.out = prcomp(x)
summary(pr.out)

# plot the first two principal component score vectors
biplot(pr.out)

# (c) perform K-means with K=3
km3.out = kmeans(x,3,nstart=30)
table(km3.out$cluster,c(rep(1,20),rep(2,20),rep(3,20)))

# (d) perform K-means with K=2
km2.out = kmeans(x,2,nstart=30)
table(km2.out$cluster,c(rep(1,20),rep(2,20),rep(3,20)))

# (e) perform K-means with K=4
km4.out = kmeans(x,4,nstart=30)
table(km4.out$cluster,c(rep(1,20),rep(2,20),rep(3,20)))

# (f) perform K-means with K=3 on the first 2 principal component vecs
km3_2.out = kmeans(pr.out$x[,1:2],3,nstart=30)
table(km3_2.out$cluster,c(rep(1,20),rep(2,20),rep(3,20)))

# (g) scale each variable to have sd=1 and then use K-means with K=3
km3_scale.out = kmeans(scale(x),3,nstart=30)
table(km3_scale.out$cluster,c(rep(1,20),rep(2,20),rep(3,20)))

