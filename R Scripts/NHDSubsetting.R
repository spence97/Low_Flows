require(rgdal)

fgdb = "C:/Users/Spencer/Documents/Research/SI/nwm_v11.gdb"
setwd = "C:/Users/Spencer/Documents/Research/SI/GitHub/Low_Flows/Low_Flows/NWM_Retro_Analysis"


# List all feature classes in a file geodatabase
subset(ogrDrivers(), grepl("GDB", name))
fc_list = ogrListLayers(fgdb)
print(fc_list)

# Read in the States and NHD stream network feature classes
States = readOGR(dsn=fgdb,layer="States")
NHD = readOGR(dsn=fgdb,layer="channels_nwm_v11_routeLink")

# Select state of interest and plot it
State_Select = States[which(States$STATE_ABBR=="CA"),]

# Subset the NHD stream network to the boundary of the state selected above
library(rgeos)
stream_subset = NHD[State_Select,]

# Subset the NHD stream network in the state by a user defined stream order then overlay the streams on the state map
stream_subset = stream_subset[stream_subset$order_ > 3,]

# Subset the above subset to select only the streams in NHD that have a corresponding USGS gage
stream_subset = stream_subset[(stream_subset$gages != " "),]
stream_subset$gages = factor(stream_subset$gages)

# Clean up the subset of gaged streams to ensure there are no NULL data values
library(gdata)
stream_subset$gages = trim(stream_subset$gages, recode.factor = TRUE)
stream_subset = stream_subset[(stream_subset$gages != ""),]
stream_subset = data.frame(stream_subset$gages,stream_subset$feature_id)
names(stream_subset)[1]=paste("GageID")
names(stream_subset)[2]=paste("COMID")

# Identify gages based on a user defined HDI value from a csv file containing HDI for all stream gages
HDI = read.csv("C:/Users/Spencer/Documents/Research/SI/GitHub/Low_Flows/Low_Flows/NWM_Retro_Analysis/hydro_disturb_index.csv")
HDI = subset(HDI, total_disturbance_index < 10)
HDI1 = data.frame(HDI$sitename)
names(HDI1)[1]=paste("GageID")

#Final Subset of stream reaches to only include stream reaches that meet the HDI requirement
COMID2gage_index=stream_subset[stream_subset$GageID %in% HDI1$GageID,]

# Create .csv file of COMID2gage_index data frame
write.csv(COMID2gage_index, file = "COMID2gage_CA.csv")








