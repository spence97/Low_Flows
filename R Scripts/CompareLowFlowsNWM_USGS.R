library(dataRetrieval)
library(PearsonDS)
library(dataRetrieval)
library(lubridate)
library(ggplot2)
#Load functions from CalcMonthlyStats.R script
#Threshold is either Perc5, Perc25, x7Q10, or x7Q2
gageID = "11383500"
comID = "8020924"
threshold = "7Q10"
startDate="1993-01-01"
endDate="2016-10-31"

lowFlowEval = function(gageID,comID,threshold,startDate,endDate){
  #Get discharge USGS Data
  qDataUSGS = readNWISdata(sites=gageID, service="dv",parameterCd="00060",
                           startDate=startDate,endDate=endDate)
  qDataUSGS = data.frame(Date=as.Date(qDataUSGS$dateTime),Discharge=qDataUSGS$X_00060_00003)
  qDataUSGS$Month = months(qDataUSGS$Date)
  
  #Get discharge from Historical Modeled (Retrospective) data
  qDataNWM = read.csv('~/GitHub/Low_Flows/RetrospectiveData/RetroRecord_cfs.csv')
  qDataNWM$Date = as.Date(qDataNWM$Date, format="%m/%d/%Y")
  comID_column = paste0("X",comID)
  qDataNWM = qDataNWM[,(names(qDataNWM) %in% c("Date",comID_column))]
  colnames(qDataNWM) = c("Date","Discharge")
  qDataNWM$Month = months(qDataNWM$Date)
  
  #Calculate monthly low-flow thresholds
  USGS_results = USGS_Stats(gageID,startDate,endDate)
  NWM_results = NWM_Stats(comID)
  
  #Calculate how often the streamflow (observed and modeled) went below a threshold
  years = seq(year(startDate),year(endDate),by=1)
  belowthreshold = function(qDF,statsDF,threshold){
    lowFlowEvents = data.frame(Year=sort(rep(years,12)),Month=rep(month.name,12),Date=as.yearmon(paste0(lowFlowEventsUSGS$Year,"-",lowFlowEventsUSGS$Month),format="%Y-%B"))
    for (m in month.name){
      qDFsub = qDF[(qDF$Month==m),]
      qDFsub$Year = year(qDFsub$Date)
      tempthreshold = statsDF[(statsDF$Month==m),threshold]
      
      for (i in unique(qDFsub$Year)){
        qDFsubyear = qDFsub[(qDFsub$Year==i),]
        numbelow = sum(qDFsubyear$Discharge < tempthreshold)
        lowFlowEvents[(lowFlowEvents$Year==i & lowFlowEvents$Month==m),"NumEvents"] = numbelow
      }
    }
    return(lowFlowEvents)
  }
  lowFlowEventsUSGS = belowthreshold(qDF = qDataUSGS, statsDF = USGS_results, threshold = threshold)
  lowFlowEventsNWM = belowthreshold(qDF = qDataNWM, statsDF = NWM_results, threshold = threshold)
  lowFlowSummary = data.frame(Year=sort(rep(years,12)),Month=rep(month.name,12),DiffEvents = lowFlowEventsUSGS$NumEvents-lowFlowEventsNWM$NumEvents)
  ggplot()+
    geom_line(aes(x=lowFlowEventsUSGS$Date,y=lowFlowSummary$DiffEvents))+
    ylab("Difference in Number of Low Flow Events")+xlab("Time")+
    ggtitle(paste0("Low-Flow Threshold:",threshold))+
    theme_bw()
  
  plot(x=lowFlowEventsUSGS$Date,y=lowFlowEventsUSGS$NumEvents,type='l',col=1,main=paste0("Low-Flow Threshold:",threshold),ylab="Number of Low Flow Events",xlab="Time")
  lines(x=lowFlowEventsNWM$Date,y=lowFlowEventsNWM$NumEvents,col=2)
}



