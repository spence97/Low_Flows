library(ncdf4)
#Set working directory to folder with a year of NetCDF data
directory=getwd()
#Set reach (From list of subsetted reaches/gages)
comid=22548559

hourList=sprintf("%02d",seq(0,23,by=1))
year=substr(directory,nchar(directory)-4+1, nchar(directory))
is.leapyear=function(year){
  return(((year %% 4 == 0) & (year %% 100 != 0)) | (year %% 400 == 0))
}
dates=read.csv('C:/Users/carly/Desktop/SummerInstitute/DateList.csv')
if (is.leapyear(as.numeric(year))){
  dateList=sprintf("%04d",dates$LeapYear)
}else{
  dateList=sprintf("%04d",dates$NonLeapYear) 
  dateList=dateList[(dateList!="  NA")]
}

#Cycle through the hourly time steps and convert to daily
ncdfFileList=shell('dir /b', intern=TRUE)
start.time = Sys.time()
dailyQDF=data.frame(Date=dateList)
for (y in dateList){
  hourlyQDF=data.frame(Hour=hourList)
  for (x in hourList){
    ncdfFileName=paste0(year,y,x,"00_streamflow.nc")
    ncdfFile=paste0(directory,"/",ncdfFileName)
    nwmFile=nc_open(ncdfFile,readunlim=FALSE)
    #Get index of COMID from netcdf (dim=1 is the stream reach)
    featureIDList=nwmFile$dim$feature_id$vals
    featureIndex=match(comid,featureIDList)
    
    #Get streamflow (in cms)
    nwmData=ncvar_get(nwmFile,
                   varid="streamflow",
                   start=c(featureIndex,1), #Start value for dimensions (first value is stream reach index)
                   count = c(1,-1)) #Number of values to get in each dimension
    nc_close(nwmFile)
    hourlyQDF[(hourlyQDF$Hour==x),"Reach"]=nwmData
  }
  meanDailyQ=mean(hourlyQDF$Reach)
  dailyQDF[(dailyQDF$Date==y),"Reach"]=meanDailyQ
}
names(dailyQDF)[ncol(dailyQDF)]=comid

end.time = Sys.time()
time.taken = end.time - start.time
time.taken

write.csv(dailyQDF,file=paste0("C:/Users/carly/Desktop/SummerInstitute/",year,".csv"),row.names=FALSE)

