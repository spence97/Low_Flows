#USGS site identification number (Enter the Gauge number(8 or 7 digits number):
Gauge_Id<-04085427
#Enter the quantile value for baseflow definition (Default is 0.05) 
Q<-0.05
#Changes the format from ABCD to "ABCD" and adds 0 to begining of gauge id if it starts with 0.
if (floor(Gauge_Id/10000000)>0) {site_id<-paste0("",Gauge_Id)
}else{
  site_id<-paste0("",Gauge_Id)
  site_id<-paste0("0",site_id)
}
# The begining date is set to 1900/01/01 and the end date is the last date with the available data in the website
startDate <- '1900-01-01'
endDate <- ''
# Setting parameters:
# 00010 ==>	Temperature, water, degrees Celsius
# 00060 ==>	Discharge, cubic feet per second	
# 00300 ==>	Non-metals	Dissolved oxygen, water, unfiltered, milligrams per liter
RequiredData<-c('00010','00060','00300')

#Fetching Data (statCd='00003' = Daily Average)
RawDailyData <- readNWISdv(site_id,RequiredData,startDate, endDate, statCd='00003')
Date<-RawDailyData[,3]
Temp<-RawDailyData[,4]
Disch<-RawDailyData[,5]
DisOxy<-RawDailyData[,6]
#How many of data for Temperature, Discharge and Dissolved oxygen are NA
Te<-as.matrix(Temp)
Di<-as.matrix(Disch)
Dis<-as.matrix(DisOxy)
Temp_NA_Percent<-(sum(is.na(Te))/nrow(Te))*100
Disch_NA_Percent<-(sum(is.na(Di))/nrow(Di))*100
DisOxy_NA_Percent<-(sum(is.na(Dis))/nrow(Dis))*100

#Building Data frame
Data_Raw<-data.frame(site_id,Date,Temp,Disch,DisOxy)

# Calculating Baseflow, maximum, minimum, average and median flow in the stream (ft^3/s)

BaseFLow<-quantile(RawDailyData[,5],na.rm = TRUE, Q)
BaseFLow<-as.numeric(BaseFLow)
Max<-max(RawDailyData[,5],na.rm = TRUE)
Min<-min(RawDailyData[,5],na.rm = TRUE)
Average<-mean(RawDailyData[,5],na.rm = TRUE)
Median<-median(RawDailyData[,5],na.rm = TRUE)

#Results in notepad format,in the directory a file named the gauge number will be produced with all of the result + summary
write.table(Data_Raw,site_id,quote=FALSE,append=FALSE,sep=" | ",row.names=FALSE)

write("========================Summary for flow========================",site_id,append=TRUE)
write("Base Flow (cfs) = ",site_id,append=TRUE)
write(BaseFLow,site_id,append=TRUE)
write("Maximum Flow (cfs) = ",site_id,append=TRUE)
write(Max,site_id,append=TRUE)
write("Minimum Flow (cfs) = ",site_id,append=TRUE)
write(Min,site_id,append=TRUE)
write("Average Flow (cfs) = ",site_id,append=TRUE)
write(Average,site_id,append=TRUE)
write("Median Flow (cfs) = ",site_id,append=TRUE)
write(Median,site_id,append=TRUE)
write("========================Summary Data Availability========================",site_id,append=TRUE)

write("Percent of available daily data for Temperature in this station = ",site_id,append=TRUE)
write(round((100-Temp_NA_Percent)),site_id,append=TRUE)

write("Percent of available daily data for Discharge in this station = ",site_id,append=TRUE)
write(round((100-Disch_NA_Percent)),site_id,append=TRUE)

write("Percent of available daily data for Dissolved oxygen in this station = ",site_id,append=TRUE)
write(round((100-DisOxy_NA_Percent)),site_id,append=TRUE)


