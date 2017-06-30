library(hydrostats)
fake.df = data.frame(date=seq(as.Date("1993-01-01"),as.Date("1993-01-31"),by=1),
                  gage1=runif(31,min=1,max=10),gage2=runif(31,min=3,max=30))

#Applies percentile function to all gage/reach records in a data frame
#Data frame must follow the structure: 1st column = Date, 2nd-nth column = streamflow series
calc_percentile = function(my.df){
  
  perc.rank <- function(x) (trunc(rank(x))/length(x))*100
  perc.df = data.frame(apply(fakedf[,-1],2, perc.rank))
  return(perc.df)
}

perc.df=calc_percentile(fakedf)

#Calculates min, max, and average
calc_stats = function(my.df){
  historicnorms = data.frame(Min=apply(my.df[,-1],2,min),
                             Avg=colMeans(my.df[,-1]),
                             Max=apply(my.df[,-1],2,max))
  return(historicnorms)
}

stat.df=calc_stats(fakedf)






