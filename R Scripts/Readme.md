Collection of scripts used in analysis of historical NWM output. 
These scripts could be used for exploring the retrospective runs of previous versions of the NWM, short-term (~5 year) historical runs (of all NWM versions), or short-term (~60 days) historical results of NWM.

Script Name | Function
------------|---------
NetCDFProcessing.R | Aggregates hourly NWM streamflow data for a number of user-specified stream reaches. Processes a single year's data files at a time.
Data Fetch.R |
StreamGage.R | Takes the full NHD stream reach feature class and subsets based on State boundary, stream order, and Hydrologic Disturbance Index (HDI) and returns a csv file linking COMID to gageID for the subsetted stream reaches.
