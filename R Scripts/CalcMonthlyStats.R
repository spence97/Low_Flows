library(PearsonDS)
library(dataRetrieval)
month="January"


USGS_Stats = function(gageID,month){
  qData = readNWISdata(sites=gageID, service="dv",parameterCd="00060",
                       startDate="1993-01-01",endDate="2016-10-01")
  #Calculate monthly statistics
  qData$Month = months(qData$dateTime)
  monthlyQStats = data.frame(Month = month,Min=NA,Avg=NA,Max=NA,Perc5=NA,Perc25=NA,x7Q10=NA,x7Q2=NA)
  #Read in discharge data
    q = qData[(qData$Month==month),"X_00060_00003"]
    #Use Log-Pearson Type III Distribution. See: https://pubs.usgs.gov/sir/2008/5126/section3.html and
    #http://deq1.bse.vt.edu/sifnwiki/index.php/R_iha_7q10#PearsonDS_function_details for the details on this function
    logq=log(q)
    pars = PearsonDS:::pearsonIIIfitML(logq)
    x7Q2 = exp(qpearsonIII(0.5, params = pars$par))
    x7Q10 = exp(qpearsonIII(0.1, params = pars$par))
    min = min(q)
    avg = mean(q)
    max = max(q)
    perc5 = quantile(q,na.rm = TRUE, probs=0.05)
    perc25 = quantile(q,na.rm = TRUE, probs=0.25)
    monthlyQStats[(monthlyQStats$Month==month),c("Min","Avg","Max","Perc5","Perc25","x7Q10","x7Q2")]=c(min,avg,max,perc5,perc25,x7Q10,x7Q2)
  return(monthlyQStats)
}


NWM_Stats = function(comID,month){

  qData = read.csv('~/GitHub/Low_Flows/RetrospectiveData/RetroRecord_cfs.csv')
  comID_column=paste0("X",comID)
  #Calculate monthly statistics
  qData$Month = months(as.Date(qData$Date,format="%m/%d/%Y"))
  monthlyQStats = data.frame(Month = month,Min=NA,Avg=NA,Max=NA,Perc5=NA,Perc25=NA,x7Q10=NA,x7Q2=NA)
  #Read in discharge data
    q = qData[(qData$Month==i),comID_column]
    #Use Log-Pearson Type III Distribution. See: https://pubs.usgs.gov/sir/2008/5126/section3.html and
    #http://deq1.bse.vt.edu/sifnwiki/index.php/R_iha_7q10#PearsonDS_function_details for the details on this function
    logq=log(q)
    pars = PearsonDS:::pearsonIIIfitML(logq)
    x7Q2 = exp(qpearsonIII(0.5, params = pars$par))
    x7Q10 = exp(qpearsonIII(0.1, params = pars$par))
    min = min(q)
    avg = mean(q)
    max = max(q)
    perc5 = quantile(q,na.rm = TRUE, probs=0.05)
    perc25 = quantile(q,na.rm = TRUE, probs=0.25)
    monthlyQStats[(monthlyQStats$Month==month),c("Min","Avg","Max","Perc5","Perc25","x7Q10","x7Q2")]=c(min,avg,max,perc5,perc25,x7Q10,x7Q2)
  return(monthlyQStats)
}

gageID="11383500"
comID="8020924"
USGS_results=USGS_Stats(gageID,month)
NWM_results=NWM_Stats(comID,month)

