import datetime as dt
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import plotly
import plotly.graph_objs as go
from tethys_sdk.gizmos import *
from .helpers import get_nwm_forecast

plotly.tools.set_credentials_file(username='spence97', api_key='y5y3btGzgv2KE5iNvebM')

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
        maxZoom=18,
        minZoom=2
    )

    NHD_Streams = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:channels_nwm_v11_routeLink'}},
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    DeerCreek_Streams = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:NHDSubset_DeerCreek'}},
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

    SantaYnez_Streams = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:NHDSubset_SantaYnez'}},
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

    SipseyFork_Streams = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:NHDSubset_SipseyFork'}},
        legend_title='NHD streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True,
        geometry_attribute='the_geom'
    )

    SipseyFork_Gage = MVLayer(
        source='ImageWMS',
        options={'url': 'http://localhost:8080/geoserver/wms',
                 'params': {'LAYERS': 'lowflows:USGSgage_SipseyFork'}},
        legend_title='NHD streams',
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
        display_text='Load Watershed',
        href = reverse('low_flows:add_watershed')
    )

    view_watershed = SelectInput(display_text='Select Watershed',
                            name='watershedselect',
                            multiple=False,
                            options=[('Full NHD Stream Network','NHD'), ('Deer Creek','DeerCreek'), ('Santa Ynez', 'SantaYnez'), ('Sipsey Fork', 'SipseyFork')],
                            initial=['', ''],
                            select2_options={'placeholder': 'Select a watershed',
                                             'allowClear': True}

    )

    stats_select = SelectInput(display_text='Select low flow statistical method',
                            name='stats_select',
                            multiple=False,
                            options=[('7Q10', '7Q10'), ('Percentiles', 'Percentiles'), ('Custom amount', 'Custom')],
                            initial=['',''],
                            select2_options={'placeholder': 'Select a low flow warning method',
                                             'allowClear': True}
    )

    custom_amt = TableView(column_names=('COMID', 'Low Flow'),
                            rows=[('', '')],
                            hover=True,
                            striped=True,
                            bordered=True,
                            condensed=True,
                            editable_columns = ('COMIDInput', 'threshInput')
    )

    show_wq = ToggleSwitch(
        name='togglewq',
        display_text='Real-time Water Quality Data'
    )

    show_rtq = ToggleSwitch(
        name='togglertq',
        display_text='Real-time Streamflow Data'
    )

    view_forecast_button = Button(
        display_text='View Forecast',
        name='view_forecast_button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('low_flows:forecast')
    )

    view_tutorial_button = Button(
        display_text='View Forecast',
        name='view_tutorial_button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('low_flows:Tutorial')
    )


    context = {
        'load_watershed':load_watershed,
        'view_watershed':view_watershed,
        'stats_select':stats_select,
        'custom_amt':custom_amt,
        'show_wq':show_wq,
        'show_rtq':show_rtq,
        'watershed_map': watershed_map,
        'view_forecast_button': view_forecast_button,
        'view_tutorial_button': view_tutorial_button
    }

    return render(request, 'low_flows/home.html', context)

@login_required()
def forecast(request):
    """
    Controller for the Forecast Viewer page.
    """


    # setup some variables to process the date and time series values
    dateraw = []
    date1 = []
    value1 = []
    date2 = []
    value2 = []
    comid = '8020924'
    # The different configurations are short_range, medium_range, or analysis_assim
    config = 'medium_range'
    startdate = '2017-07-11'
    enddate = '2017-07-20'
    forecasttime = '00'
    # call the function we set up above to get the first forecast
    watermlstring = str(get_nwm_forecast(config, comid, startdate, enddate, forecasttime))
    # print (watermlstring)
    waterml = watermlstring.split('dateTimeUTC="')
    # print ('')
    # print (waterml[0])
    # print ('')
    # print (waterml[1])
    waterml.pop(0)
    # process the first forecast
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        value1.append(parser[1].split('<')[0])
        value2.append(70)

    for e in dateraw:
        date1.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
        date2.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))

    print(value1)
    print(date1)
    print(value2)
    print(date2)

    data1 = go.Scatter(x=date1, y=value1, name='forecast')
    data2 = go.Scatter(x=date2, y=value2, name='threshold')

    data=[data1,data2]
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