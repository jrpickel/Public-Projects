SampleVariance = function(x,method="naive")
{
  if(method=="naive")
  {
    n = 0
    sum_ = 0
    sumSq = 0
    for(i in x){
      n = n + 1
      sum_ = sum_ + i
      sumSq = sumSq + i * i
    }
    variance = (sumSq-(sum_*sum_)/n)/(n-1)
    result = data.frame(sum_=sum_,sumSq=sumSq,variance=variance)
  }
  else
  {
    # two-pass algorithm
    n = 0
    sum1 = 0
    sum2 = 0
    for(i in x)
    {
      n = n + 1
      sum1 = sum1 + i
    }
    mean_ = sum1/n
    for(i in x)
    {
      sum2 = sum2 + (i-mean_)*(i-mean_)
    }
    variance = sum2 / (n-1)
    result = data.frame(sum = sum1,sum2 = sum2,variance = variance);
  }
  variance;      
}

# colVars take sin a data frame object (df) and calculates the variance of all columns
# colVars returns a vector of the variances
colstats = function(df,method="naive"){
  vals = list()
  vals$Mean = c()
  vals$Max = c()
  vals$Min = c()
  vals$Median = c()
  vals$SD = c()
  vals$Shapiro = c()
  
  cols.to.calc = df[sapply(df,is.numeric)]
  for (i in colnames(cols.to.calc)){
    temp = df[,i]
    vals$Mean = c(vals$Mean,mean(temp))
    vals$Max = c(vals$Max,max(temp))
    vals$Min = c(vals$Min,min(temp))
    vals$Median = c(vals$Median,median(temp))
    vals$SD = c(vals$SD,sqrt(SampleVariance(temp,method)))
  }
  vals
}

normalize = function(df){
  cols.to.calc = df[sapply(df,is.numeric)] 
  for(i in colnames(cols.to.calc)){
    df[i] = (df[i] - min(df[,i]))/(max(df[,i]) - min(df[,i]))
  }
  df[sapply(df,is.numeric)]
}
