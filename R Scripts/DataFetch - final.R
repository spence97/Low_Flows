#Installing and loading dataRetrieval Package.
#install.packages("dataRetrieval")
library("dataRetrieval")
### === === === === === === === === === === === ===TEMPERATURE=== === === === === === === === === === === ###
#Reading data and making output matrix (or .csv file)
#rm(list=ls())
start.time <- Sys.time()
# Reads the csv format of data, with the first column=USGS Gauges and Second column=COM Id
Raw_Data=read.csv(file="CAL.csv")
attach(Raw_Data)
N<-length(Raw_Data[,1])
Output_CA=matrix(0,nrow=N, ncol=117)
###### Naming the columns (Discharge, Temperature, DO, Min, Max, Ave, and ...)
colnames(Output_CA) <- c("Number","USGS_ID","COM_ID",
                      
                      "Min_Dis_Jan","Min_Dis_Feb","Min_Dis_Mar","Min_Dis_Apr","Min_Dis_May","Min_Dis_Jun","Min_Dis_Jul","Min_Dis_Aug",
                      "Min_Dis_Sep","Min_Dis_Oct","Min_Dis_Nov","Min_Dis_Dec",
                      "Max_Dis_Jan","Max_Dis_Feb","Max_Dis_Mar","Max_Dis_Apr","Max_Dis_May","Max_Dis_Jun","Max_Dis_Jul","Max_Dis_Aug",
                      "Max_Dis_Sep","Max_Dis_Oct","Max_Dis_Nov","Max_Dis_Dec",
                      "Ave_Dis_Jan","Ave_Dis_Feb","Ave_Dis_Mar","Ave_Dis_Apr","Ave_Dis_May","Ave_Dis_Jun","Ave_Dis_Jul","Ave_Dis_Aug",
                      "Ave_Dis_Sep","Ave_Dis_Oct","Ave_Dis_Nov","Ave_Dis_Dec",
                      
                      "Min_Temp_Jan","Min_Temp_Feb","Min_Temp_Mar","Min_Temp_Apr","Min_Temp_May","Min_Temp_Jun","Min_Temp_Jul","Min_Temp_Aug",
                      "Min_Temp_Sep","Min_Temp_Oct","Min_Temp_Nov","Min_Temp_Dec",
                      "Max_Temp_Jan","Max_Temp_Feb","Max_Temp_Mar","Max_Temp_Apr","Max_Temp_May","Max_Temp_Jun","Max_Temp_Jul","Max_Temp_Aug",
                      "Max_Temp_Sep","Max_Temp_Oct","Max_Temp_Nov","Max_Temp_Dec",
                      "Ave_Temp_Jan","Ave_Temp_Feb","Ave_Temp_Mar","Ave_Temp_Apr","Ave_Temp_May","Ave_Temp_Jun","Ave_Temp_Jul","Ave_Temp_Aug",
                      "Ave_Temp_Sep","Ave_Temp_Oct","Ave_Temp_Nov","Ave_Temp_Dec",
                      
                      "Min_Do_Jan","Min_Do_Feb","Min_Do_Mar","Min_Do_Apr","Min_Do_May","Min_Do_Jun","Min_Do_Jul","Min_Do_Aug",
                      "Min_Do_Sep","Min_Do_Oct","Min_Do_Nov","Min_Do_Dec",
                      "Max_Do_Jan","Max_Do_Feb","Max_Do_Mar","Max_Do_Apr","Max_Do_May","Max_Do_Jun","Max_Do_Jul","Max_Do_Aug",
                      "Max_Do_Sep","Max_Do_Oct","Max_Do_Nov","Max_Do_Dec",
                      "Ave_Do_Jan","Ave_Do_Feb","Ave_Do_Mar","Ave_Do_Apr","Ave_Do_May","Ave_Do_Jun","Ave_Do_Jul","Ave_Do_Aug",
                      "Ave_Do_Sep","Ave_Do_Oct","Ave_Do_Nov","Ave_Do_Dec",
                      
                      "Base_Dis_5%", "Base_Dis_25%",
                      "Dis_Avail_Data_%","Temp_Avail_Data_%","DO_Avail_Data_%",
                      "HDI")

Output_CA[,1]<-c(1:N)
Output_CA[,2]<-Raw_Data[,1]
Output_CA[,3]<-Raw_Data[,2]
Output_CA[,117]<-Raw_Data[,3]

#####
# Column Labeling and initial assignment, Start and End Datesand etc
startDate <- '1993-01-01'
endDate <- '2016-10-31'

#Defining Quantiles
Q1<-0.05
Q2<-0.25
# Setting parameters:
# 00010 ==>	Temperature, water, degrees Celsius
# 00060 ==>	Discharge, cubic feet per second	
# 00300 ==>	Non-metals	Dissolved oxygen, water, unfiltered, milligrams per liter
RequiredData<-c('00010','00060','00300')
#####
#USGS site identification number (Enter the Gauge number(8 or 7 digits number):
Gauge_Id<-matrix(0,ncol=1,nrow=N)
site_id<-matrix(0,ncol=1,nrow=N)

for (i in 1:N) {
#Reading gauge ID    
Gauge_Id[i]<-as.numeric(Output_CA[i,2])
#Changes the format from ABCD to "ABCD" and adds 0 to begining of gauge id if it starts with 0.
if (floor(Gauge_Id[i]/10000000)>0) {site_id[i]<-paste0("",Gauge_Id[i])
}else{
  site_id[i]<-paste0("",Gauge_Id[i])
  site_id[i]<-paste0("0",site_id[i])
}

RawDailyData<- readNWISdv(site_id[i],RequiredData,startDate, endDate, statCd='00003')

if (ncol(RawDailyData)==0) {Output_CA[i,4:116]<-NA } else {


Date<-RawDailyData[,"Date"]

if("X_00010_00003" %in% colnames(RawDailyData))
{
  Temp<-(RawDailyData[,"X_00010_00003"])
} else {Temp<-matrix(NA,nrow =length(Date))}

if("X_00060_00003" %in% colnames(RawDailyData))
{
  Disch<-(RawDailyData[,"X_00060_00003"])
} else {Disch<-matrix(NA,nrow =length(Date))}


if("X_00300_00003" %in% colnames(RawDailyData))
{
  DisOxy<-(RawDailyData[,"X_00300_00003"])
} else {DisOxy<-matrix(NA,nrow =length(Date))}

All<-data.frame(Date,Temp,Disch,DisOxy)
}

####
for (j in (1:12)){
Output_CA[i,j+3]<-min(All[which(as.numeric(format(All[,1], "%m"))==j),3],na.rm = TRUE)
Output_CA[i,j+15]<-max(All[which(as.numeric(format(All[,1], "%m"))==j),3],na.rm = TRUE)
Output_CA[i,j+27]<-mean(All[which(as.numeric(format(All[,1], "%m"))==j),3],na.rm = TRUE)


Output_CA[i,j+39]<-min(All[which(as.numeric(format(All[,1], "%m"))==j),2],na.rm = TRUE)
Output_CA[i,j+51]<-max(All[which(as.numeric(format(All[,1], "%m"))==j),2],na.rm = TRUE)
Output_CA[i,j+63]<-mean(All[which(as.numeric(format(All[,1], "%m"))==j),2],na.rm = TRUE)


Output_CA[i,j+75]<-min(All[which(as.numeric(format(All[,1], "%m"))==j),4],na.rm = TRUE)
Output_CA[i,j+87]<-max(All[which(as.numeric(format(All[,1], "%m"))==j),4],na.rm = TRUE)
Output_CA[i,j+99]<-mean(All[which(as.numeric(format(All[,1], "%m"))==j),4],na.rm = TRUE)

Output_CA[i,112]<-quantile(Disch,na.rm = TRUE, Q1)
Output_CA[i,113]<-quantile(Disch,na.rm = TRUE, Q2)


Output_CA[i,114]<-100-((sum(is.na(Disch))/length(Disch))*100)
Output_CA[i,115]<-100-((sum(is.na(Temp))/length(Disch))*100)
Output_CA[i,116]<-100-((sum(is.na(DisOxy))/length(Disch))*100)
}
#####

#rm(RawDailyData,Date,Temp,Disch,DisOxy)
}

#options(warn=-1)


Output_CA[is.nan(Output_CA)]<-NA
Output_CA[is.infinite(Output_CA)]<-NA


end.time <- Sys.time()
Duration<-end.time-start.time
Duration

write.table(Output_CA,"site_id_CA",quote=FALSE,append=FALSE,sep=" | ",row.names=FALSE)
write.csv(Output_CA, file = "Cal_USGS.csv")


