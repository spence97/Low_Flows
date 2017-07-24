import os
import json
import datetime as dt
import random
import csv
from pprint import pprint
from datetime import datetime, timedelta
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import plotly
import plotly.graph_objs as go
from tethys_sdk.gizmos import *
from .helpers import get_nwm_forecast
from .app import LowFlows as app


plotly.tools.set_credentials_file(username='spence97', api_key='y5y3btGzgv2KE5iNvebM')

#Get current month for looking up threshold
currentMonthNumber = datetime.now().month

WORKSPACE = 'low_flows'
GEOSERVER_URI = 'tethys.byu.edu/apps/lowflows'

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Define view options
    view_options = MVView(
        projection='EPSG:4326',
        center=[-100,40],
        zoom=5,
        maxZoom=15,
        minZoom=2
    )

    # Full NHD Stream Layer (Higher than stream order 2)

    NHD_Streams = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:NHD_Streams'}},
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    # Deer Creek, Northern California

    # Get path to Deer Creek GeoJson
    app_workspace = app.get_app_workspace()
    deercreek_json_path = os.path.join(app_workspace.path, 'GeoJSONFiles', 'NHDSubset_DeerCreek.geojson')
    deercreek_json_string = ''

    # Open the GeoJson
    with open(deercreek_json_path, 'r') as deercreek_json_file:
        for line in deercreek_json_file.readlines():
            deercreek_json_string += line.strip()

    # Convert to GeoJson dictionary
    deercreek_json = json.loads(deercreek_json_string.strip())

    # Add stats properties
    for feature in deercreek_json['features']:
        filename = 'X' + str(feature['properties']['feature_id']) + '.csv'
        deercreek_stat_path = os.path.join(app_workspace.path, 'StatsFiles','DeerCreek', filename)
        with open(deercreek_stat_path, 'r') as deercreek_stat_file:
            monthlystats = csv.reader(deercreek_stat_file, delimiter=',', quotechar='|')
            monthlystats = list(monthlystats)
            statinfo = monthlystats[currentMonthNumber]
        feature['properties']['x7q10'] = statinfo[7] # From CSVs
        feature['properties']['x7q2'] = statinfo[8] # From CSVs
        feature['properties']['perc5'] = statinfo[5] # From CSVs
        feature['properties']['perc25'] = statinfo[6] # From CSVs
        feature['properties']['min_forecast_flow'] = random.uniform(0, 20) # derived from forecast

    DeerCreek_Streams = MVLayer(
        source='GeoJSON',
        options=deercreek_json,
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    DeerCreek_Gage = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:USGSgage_DeerCreek'}},
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    DeerCreek_Boundary = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:Watershed_DeerCreek'}},
        legend_title='Watershed Boundary',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=False
    )

    

    # Santa Ynez

    # Get path to Santa Ynez GeoJson
    app_workspace = app.get_app_workspace()
    santaynez_json_path = os.path.join(app_workspace.path, 'GeoJSONFiles', 'NHDSubset_SantaYnez.geojson')
    santaynez_json_string = ''

    # Open the GeoJson
    with open(santaynez_json_path, 'r') as santaynez_json_file:
        for line in santaynez_json_file.readlines():
            santaynez_json_string += line.strip()

    # Convert to GeoJson dictionary
    santaynez_json = json.loads(santaynez_json_string.strip())

    # Add stats properties
    for feature in santaynez_json['features']:
        feature['properties']['x7q10'] = random.uniform(0, 5) # From CSVs
        feature['properties']['x7q2'] = random.uniform(0, 10) # From CSVs
        feature['properties']['perc5'] = random.uniform(0, 5) # From CSVs
        feature['properties']['perc25'] = random.uniform(0, 10) # From CSVs
        feature['properties']['min_forecast_flow'] = random.uniform(0, 7) # derived from forecast


    SantaYnez_Streams = MVLayer(
        source='GeoJSON',
        options=santaynez_json,
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    SantaYnez_Gage = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:USGSgage_SantaYnez'}},
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    SantaYnez_Boundary = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:Watershed_SantaYnez'}},
        legend_title='Watershed Boundary',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=False
    )

    # Sipsey Fork

    # Get path to Sipsey Fork GeoJson
    app_workspace = app.get_app_workspace()
    sipsey_json_path = os.path.join(app_workspace.path, 'GeoJSONFiles', 'NHDSubset_SipseyFork.geojson')
    sipsey_json_string = ''

    # Open the GeoJson
    with open(sipsey_json_path, 'r') as sipsey_json_file:
        for line in sipsey_json_file.readlines():
            sipsey_json_string += line.strip()

    # Convert to GeoJson dictionary
    sipsey_json = json.loads(sipsey_json_string.strip())

    # Add stats properties
    for feature in sipsey_json['features']:
        filename = 'X' + str(feature['properties']['feature_id']) + '.csv'
        sipsey_stat_path = os.path.join(app_workspace.path, 'StatsFiles','SipseyFork', filename)
        with open(sipsey_stat_path, 'r') as sipsey_stat_file:
            monthlystats = csv.reader(sipsey_stat_file, delimiter=',', quotechar='|')
            monthlystats = list(monthlystats)
            statinfo = monthlystats[currentMonthNumber]
        feature['properties']['x7q10'] = statinfo[7] # From CSVs
        feature['properties']['x7q2'] = statinfo[8] # From CSVs
        feature['properties']['perc5'] = statinfo[5] # From CSVs
        feature['properties']['perc25'] = statinfo[6] # From CSVs
        feature['properties']['min_forecast_flow'] = random.uniform(0, 7) # derived from forecast


    SipseyFork_Streams = MVLayer(
        source='GeoJSON',
        options=sipsey_json,
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    SipseyFork_Gage = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:USGSgage_SipseyFork'}},
        legend_title='USGS Gage',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    SipseyFork_Boundary = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params':{'LAYERS': 'lowflows:Watershed_SipseyFork'}},
        legend_title='Watershed Boundary',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=False
    )

    # Define map view options
    watershed_map = MapView(
        height='100%',
        width='100%',
        controls=['ZoomSlider', 'Rotate', 'FullScreen'],
        layers=[NHD_Streams, DeerCreek_Streams, DeerCreek_Gage, DeerCreek_Boundary, SantaYnez_Streams, SantaYnez_Gage, SantaYnez_Boundary, SipseyFork_Streams, SipseyFork_Gage, SipseyFork_Boundary],
        view=view_options,
        basemap={'Bing': {
            'key': '5TC0yID7CYaqv3nVQLKe~xWVt4aXWMJq2Ed72cO4xsA~ApdeyQwHyH_btMjQS1NJ7OHKY8BK-W-EMQMrIavoQUMYXeZIQOUURnKGBOC7UCt4',
            'imagerySet': 'Aerial'}},
        legend=False
    )

    load_watershed = Button(
        name='load-watershed',
        display_text='Load Custom Watershed',
        href = reverse('low_flows:add_watershed'),
        icon = 'glyphicon glyphicon-plus',
        style = 'success',
    )

    view_watershed = SelectInput(display_text='Select Watershed',
                            name='watershedselect',
                            multiple=False,
                            options=[('NHD Stream Network','NHD'), ('Deer Creek','DeerCreek'), ('Santa Ynez', 'SantaYnez'), ('Sipsey Fork', 'SipseyFork')],
                            initial=['', ''],
                            select2_options={'placeholder': 'Select a watershed',
                                             'allowClear': True}

    )

    stats_select = SelectInput(display_text='Select measure of low flow',
                            name='stats_select',
                            multiple=False,
                            options=[('None', 'none'), ('7Q10', '7Q10'),('7Q2', '7Q2'), ('5th percentile', 'Perc5'), ('25th percentile', 'Perc25'), ('Custom amount', 'Custom')],
                            initial=['None'],
                            select2_options={'placeholder': 'Select a low flow threshold',
                                             'allowClear': True}


    )

    custom_amt = DataTableView(column_names=('COMID', 'Low Flow'),
                            rows=[('18578689', '10 cfs'), ('18578829','20 cfs')],
                            display_text='User-defined flow thresholds',
                            searching=False,
                            orderClasses=False,
                            lengthMenu=[[2,4,6,8,10],[2,4,6,8,10]],

    )

    add_threshold = Button(
        name='add-threshold',
        display_text='Add Custom Threshold',
        icon = 'glyphicon glyphicon-plus',
        style = 'success',
    )

    show_wq = ToggleSwitch(
        name='togglewq',
        display_text='Real-time Water Quality Data'
    )

    show_rtq = ToggleSwitch(
        name='togglertq',
        display_text='Real-time Streamflow Data'
    )


    context = {
        'load_watershed':load_watershed,
        'view_watershed':view_watershed,
        'stats_select':stats_select,
        'custom_amt':custom_amt,
        'add_threshold':add_threshold,
        'show_wq':show_wq,
        'show_rtq':show_rtq,
        'watershed_map': watershed_map
    }

    return render(request, 'low_flows/home.html', context)

@login_required()
def forecast(request):
    """
    Controller for the Forecast Viewer page.
    """

    # Set the default COMID, statistics method, and forecast lag time values
    comid = '18578689'
    stats_method = 'none'
    now = datetime.now()
    currentMonthNumber = now.month
    print(now)
    startdate = datetime.now().date().strftime('%Y-%m-%d')
    enddate = datetime.now().date().strftime('%Y-%m-%d')

    # Determine which long range forecast time to query based on the current time
    if now.hour < 13:
        forecastdate = datetime.now() - timedelta(days=1)
        startdate = forecastdate.date().strftime('%Y-%m-%d')
        enddate = forecastdate.date().strftime('%Y-%m-%d')
        print(startdate)
        print(enddate)

    else:
        startdate = datetime.now().date().strftime('%Y-%m-%d')
        enddate = datetime.now().date().strftime('%Y-%m-%d')
        print(startdate)

    # Access the selected stream's COMID and the the selected statistical threshold method
    if request.GET and 'comid' in request.GET:
        comid = request.GET.get('comid')
        stats_method = request.GET.get('stats_method')
        watershed_name = request.GET.get('watershed')

    print(stats_method)
    stats_method2 = ''

    app_workspace = app.get_app_workspace()
    statsfilename = 'X' + str(comid) + '.csv'
    UDThreshfile = 'UDThresh.csv'
    print(statsfilename)
    stat_path = os.path.join(app_workspace.path, 'StatsFiles', watershed_name, statsfilename)
    UDThresh_path = os.path.join(app_workspace.path, 'StatsFiles', watershed_name, UDThreshfile)

    with open(UDThresh_path, 'r') as UDfile:
        UDthresh = csv.reader(UDfile, delimiter=',', quotechar='|')
        COMID2thresh = [row for row in UDthresh if row[0] != int(comid)]


    with open(stat_path, 'r') as statsfile:
        monthlystats = csv.reader(statsfile, delimiter=',', quotechar='|')
        monthlystats = list(monthlystats)
        statinfo = monthlystats[currentMonthNumber]

    # setup some variables to process the date and time series values
    dateraw = []
    date1 = []
    value1 = []
    date2 = []
    value2 = []
    date3 = []
    value3 = []
    date4 = []
    value4 = []


    comid = comid
    # The different configurations are short_range, medium_range, long_range, or analysis_assim
    config = 'long_range'
    # Access the current date and create a string (YYYY-mm-dd) and use for the start date for the forecast query
    # call the function we set up above to get the first forecast
    watermlstring = str(get_nwm_forecast(config, comid, startdate, enddate))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    # process the first forecast
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        value1.append(parser[1].split('<')[0])
        if stats_method == 'none':
            value2.append('')
            value3.append('')
            stats_method2 = 'none'
        elif stats_method == '7Q2':
            value2.append(statinfo[8])
            value3.append(statinfo[7])
            stats_method2 = '7Q10'
        elif stats_method == '7Q10':
            value2.append(statinfo[8])
            value3.append(statinfo[7])
            stats_method = '7Q2'
            stats_method2 = '7Q10'
        elif stats_method == 'Perc25':
            value2.append(statinfo[6])
            value3.append(statinfo[5])
            stats_method2 = 'Perc5'
        elif stats_method == 'Perc5':
            value2.append(statinfo[6])
            value3.append(statinfo[5])
            stats_method = 'Perc25'
            stats_method2 = 'Perc5'
        elif stats_method == 'Custom':
            value2.append(COMID2thresh[1])

        if comid=='18578689':
            value4.append(10)
        elif comid=='18578829':
            value4.append(20)


    for e in dateraw:
        date1.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
        date2.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
        date3.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
        if comid=='18578689':
            date4.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
        elif comid=='18578829':
            date4.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))

    data1 = go.Scatter(x=date1, y=value1, name= 'NWM Forecast')
    data2 = go.Scatter(x=date2, y=value2, marker = dict(color = '#ff8800', line = dict(width = 4)), name= stats_method)
    data3 = go.Scatter(x=date3, y=value3, marker = dict(color = '#ad1f00', line = dict(width = 4)), name= stats_method2)
    data4 = go.Scatter(x=date4, y=value4, marker = dict(color = '#00ada1', line = dict(width = 4)), name= 'User Defined')



    if stats_method == '7Q2' or stats_method == '7Q10' or stats_method == 'Perc5' or stats_method == 'Perc25':
        data=[data1,data2,data3,data4]
    elif stats_method == 'Custom':
        data=[data1,data2,data4]
    else:
        data=[data1,data4]


    nwm_plot = PlotlyView(data)
    #Create Plotly Plot of NWM Data

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('low_flows:home')
    )

    context = {
        'cancel_button': cancel_button,
        'nwm_plot': nwm_plot
    }

    return render(request, 'low_flows/forecast.html', context)

def add_watershed(request):
    """
    Controller for the Add Watershed page.
    """

    # Default Values
    name = ''
    shapefile = ''
    statsfile = ''

    # Errors
    name_error = ''
    shape_error = ''
    stats_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        name = request.POST.get('name', None)
        shapefile = request.POST.get('shapefile', None)
        statsfile = request.POST.get('statsfile', None)

        # Validate
        if not name:
            has_errors = True
            name_error = 'Name is required.'

        if not shapefile:
            has_errors = True
            shape_error = 'A boundary shapefile is required.'

        if not statsfile:
            has_errors = True
            stats_error = 'A file linking COMID to streamflow statistics is required'

        if not has_errors:
            add_new_watershed(name=name)
            return redirect(reverse('low_flows:home'))

        messages.error(request, "Please fix errors.")

    # Define form gizmos
    watershed_name_input = TextInput(
        display_text='Watershed Name',
        name='name',
        initial=name,
        error=name_error
    )

    low_thresh_input = TableView(column_names=('COMID', 'Flow Threshold (cfs)'),
                       rows=[('', ''),('',''),('',''),('','')],
                       hover=True,
                       striped=True,
                       bordered=True,
                       editable_columns=('COMIDInput','ThreshInput'),
                       condensed=True
    )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-watershed-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('low_flows:home')
    )

    context = {
        'watershed_name_input': watershed_name_input,
        'low_thresh_input': low_thresh_input,
        'add_button': add_button,
        'cancel_button': cancel_button
    }

    return render(request, 'low_flows/add_watershed.html', context)

@login_required()
def Tutorial(request):
    """
    Controller for the Forecast Viewer page.
    """
    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('low_flows:home')
    )

    context = {
        'cancel_button': cancel_button
    }

    return render(request, 'low_flows/Tutorial.html', context)
