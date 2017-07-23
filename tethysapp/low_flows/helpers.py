import requests

# Use the API from the NWM Viewer app to get the WaterML text
def get_nwm_forecast(config, comid, startdate, enddate):
    url = 'https://appsdev.hydroshare.org/apps/nwm-forecasts/api/GetWaterML/?config=' + config + '&geom=channel_rt&variable=streamflow&COMID=' + comid + '&lon=-87.5658033081755&lat=33.2279708144365&startDate='+startdate+'&endDate='+enddate+'&time=00&lag=t00z'
    res = requests.get(url).content
    return res

