library(hydroGOF)
library(dataRetrieval)
gageID="11383500"
comID="8020924"

retroNWM_USGS_Eval = function(gageID,comID){
  #Get discharge USGS Data
  qDataUSGS = readNWISdata(sites=gageID, service="dv",parameterCd="00060",
                       startDate="1993-01-01",endDate="2016-10-31")
  qDataUSGS = data.frame(Date=as.Date(qDataUSGS$dateTime),GageDischarge=qDataUSGS$X_00060_00003)
  #Get discharge from Historical Modeled (Retrospective) data
  qDataNWM = read.csv('~/GitHub/Low_Flows/RetrospectiveData/RetroRecord_cfs.csv')
  qDataNWM$Date = as.Date(qDataNWM$Date, format="%m/%d/%Y")
  comID_column = paste0("X",comID)
  qDataNWM = qDataNWM[,(names(qDataNWM) %in% c("Date",comID_column))]
  colnames(qDataNWM)=c("Date","ModelDischarge")

  #Calculate percentile of flow from historical data
  calc_percentile = function(data,colname){
    perc.rank = (trunc(rank(data[,colname]))/length(data[,colname]))*100
    return(perc.rank)
  }
  qDataNWM$ModelQPerc = calc_percentile(data=qDataNWM,colname="ModelDischarge") 
  qDataUSGS$USGSQPerc = calc_percentile(data=qDataUSGS,colname="GageDischarge")
  
  QGOF_relative = gof(sim=qDataNWM$ModelQPerc,obs=qDataUSGS$USGSQPerc)
  QGOF_absolute = gof(sim=qDataNWM$ModelDischarge,obs=qDataUSGS$GageDischarge)
  #Graphical representation
  ggof(sim=qDataNWM$ModelQPerc,obs=qDataUSGS$USGSQPerc)
}
