import datetime as dt
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
from tethys_sdk.gizmos import MapView, MVView, MVLayer, MVLegendClass, Button, ToggleSwitch, TextInput, PlotlyView, TextInput, TableView
from .helpers import get_nwm_forecast


@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    # Define view options
    view_options = MVView(
        projection='EPSG:4326',
        center=[-100, 40],
        zoom=5,
        maxZoom=18,
        minZoom=2
    )

    NHD_Streams = MVLayer(
        source='TileArcGISRest',
        options={
            'url': 'http://geoserver.byu.edu/arcgis/rest/services/NWM/nwm_channel_v10/MapServer'},
        legend_title='NHD Streams',
        legend_extent=[-173, 17, -65, 72],
        feature_selection=True
    )

    # Define map view options
    watershed_map = MapView(
        height='100%',
        width='100%',
        controls=['ZoomSlider', 'Rotate', 'FullScreen',
                  {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
        layers=[NHD_Streams],
        view=view_options,
        basemap='OpenStreetMap',
        legend=True
    )

    load_watershed = Button(
        name='load-watershed',
        display_text='Load Watershed',
        href = reverse('low_flows:add_watershed')
    )

    zoom_watershed = Button(
        name='zoom-watershed',
        display_text='Zoom to Watershed'
    )

    show_7q10 = ToggleSwitch(
        name='toggle7q10',
        display_text='7Q10'
    )

    show_25 = ToggleSwitch(
        name='toggle25',
        display_text='25th Percentile Flow'
    )

    custom_amt = TextInput(
        name='custom_amt',
        display_text='Enter Custom Amount',
        placeholder='e.g. 30 cfs'
    )

    show_wq = ToggleSwitch(
        name='togglewq',
        display_text='Real-time Water Quality Data'
    )

    show_rtq = ToggleSwitch(
        name='togglertq',
        display_text='Real-time Streamflow'
    )

    view_forecast_button = Button(
        display_text='View Forecast',
        name='view_forecast_button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('low_flows:forecast')
    )

    context = {
        'load_watershed':load_watershed,
        'zoom_watershed':zoom_watershed,
        'show_7q10':show_7q10,
        'show_25':show_25,
        'custom_amt':custom_amt,
        'show_wq':show_wq,
        'show_rtq':show_rtq,
        'watershed_map': watershed_map,
        'view_forecast_button': view_forecast_button,
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
        value2.append(60)

    for e in dateraw:
        date1.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
        date2.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))

    print(value1)
    print(date1)

    #Create Plotly Plot of NWM Data

    nwm_plot = PlotlyView([go.Scatter(x=date1, y=value1)],[go.Scatter(x=date2,y=value2)])

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
    Controller for the Add Dam page.
    """
    # Default Values
    name = ''
    shapefile = ''
    statsfile = ''
    threshold = ''

    # Errors
    name_error = ''
    shape_error = ''
    stats_error = ''
    thresh_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        name = request.POST.get('name', None)
        shapefile = request.POST.get('shapefile', None)
        statsfile = request.POST.get('statsfile', None)
        threshold = request.POST.get('date-built', None)

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
            add_new_watershed(name=name, shapefile=shapefile, statsfile=statsfile, threshold=threshold)
            return redirect(reverse('low_flows:home'))

        messages.error(request, "Please fix errors.")

    # Define form gizmos
    watershed_name_input = TextInput(
        display_text='Watershed Name',
        name='name',
        initial=name,
        error=name_error
    )

    shapefile_input = TextInput(
        display_text='Watershed Boundary Shapefile',
        name='shapefile',
        initial=shapefile,
        placeholder='need to figure out how to upload a file and then save it to a server for future use',
        error=shape_error
    )

    statsfile_input = TextInput(
        display_text='.csv file linking COMID to streamflow stats',
        name='statsfilefile',
        initial=statsfile,
        placeholder='need to figure out how to upload a file and then save it to a server for the app to read in during future use',
        error=stats_error
    )

    low_thresh_input = TableView(column_names=('COMID', 'Flow Threshold (cfs)'),
                       rows=[('8020924', '60'),('8020864','75'),('',''),('','')],
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
        'shapefile_input': shapefile_input,
        'low_thresh_input': low_thresh_input,
        'statsfile_input': statsfile_input,
        'add_button': add_button,
        'cancel_button': cancel_button,
    }

    return render(request, 'low_flows/add_watershed.html', context)