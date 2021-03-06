library(ncdf4)

agg_hourly_streamflow = function(directory,comids,suffix){
  year=substr(directory,nchar(directory)-3,nchar(directory))
  #Create list for cycling through hourly files
  hourList=sprintf("%02d",seq(0,23,by=1))

  #Cycle through the hourly time steps and convert to daily
  ncdfFileList=shell('dir /b', intern=TRUE)
  dateList=unique(substr(ncdfFileList,5,8))
  #Initialize data frame for daily summaries
  dailyQDF=data.frame(Date = dateList)
  for (y in dateList){
    #Initialize data frame for hourly values
    hourlyQDF=data.frame(Hour=hourList)
    for (x in hourList){
      #Get and open netcdf files
      ncdfFileName=paste0(year,y,x,"00_streamflow.nc")
      ncdfFile=paste0(directory,"/",ncdfFileName)
      nwmFile=nc_open(ncdfFile,readunlim=FALSE)
      #Check if the streamflow data is missing (if so, assign NA value)
      if (nwmFile$dim$time$len==0){
        #Get index of COMID from netcdf (dim=1 is the stream reach)
        featureIDList=nwmFile$dim$feature_id$vals
        featureIndex=match(comids,featureIDList)
        for (i in featureIndex){
          hourlyQDF[(hourlyQDF$Hour==x),as.character(i)]=NA
        }
        nc_close(nwmFile)
      }else{
        #Get index of COMID from netcdf (dim=1 is the stream reach)
        featureIDList=nwmFile$dim$feature_id$vals
        featureIndex=match(comids,featureIDList)
        if (y=="0101" & x == "01"){
          dailyQDF[as.character(featureIndex)]=NA
        }
        for (i in featureIndex){
          #Get streamflow for chosen reaches(in cms)
          nwmData=ncvar_get(nwmFile,
                         varid="streamflow",
                         start=c(i,1), #Start value for dimensions (first value is stream reach index)
                         count = c(1,-1)) #Number of values to get in each dimension
          #Add hourly streamflow value to data frame
          hourlyQDF[(hourlyQDF$Hour==x),as.character(i)]=nwmData
        }
        nc_close(nwmFile)
      }
    }

    #Calculate daily mean streamflow
    meanDailyQ=colMeans(hourlyQDF[,2:length(hourlyQDF)],na.rm=TRUE)
    #Add daily mean streamflow to data frame
    dailyQDF[(dailyQDF$Date==y),c(as.character(featureIndex))]=meanDailyQ
    print(y)
  }
  #Format Date
  dailyQDF$Date=as.Date(paste0(year,"-",substr(dailyQDF$Date,1,2),"-",substr(dailyQDF$Date,3,4)))
  #Rename Columns to have COMIDs instead of index values
  names(dailyQDF)=c("Date",as.character(comids))
  #Output results to csv file
  write.csv(dailyQDF,file=paste0(directory,"/",year,suffix,".csv"),row.names=FALSE)
  return(dailyQDF)
}

#Set working directory to folder with a year of NetCDF data
directory=getwd()
#Set reach (From list of subsetted reaches/gages)
comidfile=read.csv('~/GitHub/Low_Flows/Accessory Files/COMID2gage Index Tables/CA/NHDSubsetStreamOrder3_DeerCreek.csv')
comids=comidfile$feature_id
daily_QDF=agg_hourly_streamflow(directory,comids,suffix="CA_Casestudy")
