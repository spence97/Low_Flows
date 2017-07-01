from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
from tethys_sdk.gizmos import MapView, Button, ToggleSwitch, TextInput, PlotlyView

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    watershed_map = MapView(
        height='50%',
        width='50%',
        layers=[],
        basemap='OpenStreetMap',
    )

    forecast_plot = PlotlyView(
        [go.Scatter(x=[3, 5, 7], y=[1, 3, 6])]
    )

    load_watershed = Button(
        name='load-watershed',
        display_text='Load Watershed'
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

    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
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
        'plotly_view_input':forecast_plot,
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'low_flows/home.html', context)