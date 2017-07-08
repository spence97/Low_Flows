require(rgdal)

fgdb = "C:/Users/Spencer/Documents/Research/SI/nwm_v11.gdb"
setwd = "C:/Users/Spencer/Documents/Research/SI/GitHub/Low_Flows/Low_Flows/Accessory Files"


# List all feature classes in a file geodatabase
subset(ogrDrivers(), grepl("GDB", name))
fc_list = ogrListLayers(fgdb)
print(fc_list)

# Read in the States and NHD stream network feature classes
States = readOGR(dsn=fgdb,layer="States")
NHD = readOGR(dsn=fgdb,layer="channels_nwm_v11_routeLink")

# Select state of interest and plot it
State_Select = States[which(States$STATE_ABBR=="AL"),]

# Subset the NHD stream network to the boundary of the state selected above
library(rgeos)
stream_subset_state= NHD[State_Select,]
lines(stream_subset_state)
# Subset the NHD stream network in the state by a user defined stream order then overlay the streams on the state map
stream_subset_order = stream_subset_state[stream_subset_state$order_ > 3,]

# Subset the subset_order to select only the streams in NHD that have a corresponding USGS gage
stream_subset_gage = stream_subset_order[(stream_subset_order$gages != " "),]
stream_subset_gage$gages = factor(stream_subset_gage$gages)

# Clean up the subset of gaged streams to ensure there are no NULL data values
library(gdata)
stream_subset_gage$gages = trim(stream_subset_gage$gages, recode.factor = TRUE)
stream_subset_gage = stream_subset_gage[(stream_subset_gage$gages != ""),]
stream_subset_gage = data.frame(stream_subset_gage$gages,stream_subset_gage$feature_id,stream_subset_gage$lon,stream_subset_gage$lat)
names(stream_subset_gage)[1]=paste("GageID")
names(stream_subset_gage)[2]=paste("COMID")
names(stream_subset_gage)[3]=paste("lon")
names(stream_subset_gage)[4]=paste("lat")

# Identify gages based on a user defined HDI value from a csv file containing HDI for all stream gages
HDI = read.csv("C:/Users/Spencer/Documents/Research/SI/GitHub/Low_Flows/Low_Flows/Accessory Files/hydro_disturb_index.csv")
HDI = subset(HDI, total_disturbance_index < 10)
HDI1 = data.frame(HDI$sitename)
names(HDI1)[1]=paste("sitename")

# pad the GageIDs with a leading "0" for 7 digit gageIDs
library(stringr)
HDI1 = data.frame(str_pad(HDI1$sitename,8,pad="0"))
names(HDI1)[1]=paste("GageID")

#Final Subset of stream reaches to only include stream reaches that meet the HDI requirement
stream_subset_HDI=stream_subset_gage[stream_subset_gage$GageID %in% HDI1$GageID,]

# Create .csv file of COMID2gage_index data frame
write.csv(stream_subset_HDI, file = "C:/Users/Spencer/Documents/Research/SI/GitHub/Low_Flows/Low_Flows/Accessory Files/COMID2gage Index Tables/COMID2gage_AL.csv")

# Create a point shapefile showing the final subsetted gage locations
library(sp)
coordinates(stream_subset_HDI)=3:4
plot(State_Select)
points(stream_subset_HDI)
writeOGR(stream_subset_HDI,layer='gage_locations_AL', 'C:/Users/Spencer/Documents/Research/SI/GitHub/Low_Flows/Low_Flows/Accessory Files/Shapefiles/', driver="ESRI Shapefile")






