Collection of scripts used in analysis of historical NWM output. 
These scripts could be used for exploring the retrospective runs of previous versions of the NWM, short-term (~5 year) historical runs (of all NWM versions), or short-term (~60 days) historical results of NWM.

Script Name | Function
------------|---------
NetCDFProcessing.R | Aggregates hourly NWM streamflow data for a number of user-specified stream reaches. Processes a single year's data files at a time.
Data Fetch.R | Read the final version please (DataFetch - final.R)
NHDSubsetting.R | Takes the full NHD stream reach feature class and subsets it based on state boundary, stream order, Hydrologic Disturbance Index (HDI), and USGS gage data availability.  Returns a .csv file linking COMID to gageID for the subsetted stream reaches.
DataFetch - final| Read the information for all gauges in California, starting 1993-01-01 to 2016-10-31, Including Discharge, Temperature, and DO. Then monthly statistics, including maximum, minimum, and average is calculated. For each gauge, the HDI, base flow (based on 5% quantile and 25% quantile) and finally, percentage of available data for Discharge, Temperature,and DO is calculated.
==> The result of this code is available on Google.Drive (USGS_Gauges/Cal_USGS.csv)
