from tethys_sdk.base import TethysAppBase, url_map_maker


class LowFlows(TethysAppBase):
    """
    Tethys app class for Low Flow Warning System.
    """

    name = 'Low Flow Warning System'
    index = 'low_flows:home'
    icon = 'low_flows/images/icon.gif'
    package = 'low_flows'
    root_url = 'low-flows'
    color = '#ff2a00'
    description = 'Place a brief description of your app here.'
    tags = '&quot;Hydrology&quot;,&quot;Low Flows&quot;, &quot;Drought&quot;'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (

            UrlMap(
                name='home',
                url='low-flows/home',
                controller='low_flows.controllers.home'
            ),
            UrlMap(
                name='forecast',
                url='low-flows/forecast',
                controller='low_flows.controllers.forecast'
            ),
            UrlMap(
                name='add_watershed',
                url='low-flows/watershed/add',
                controller='low_flows.controllers.add_watershed'
            ),
        )

        return url_maps


def custom_settings(self):
    """
    Example custom_settings method.
    """
    custom_settings = (
        CustomSetting(
            name='max_watersheds',
            type=CustomSetting.TYPE_INTEGER,
            description='Maximum number of watersheds that can be created in the app.',
            required=False
        ),
    )
    return custom_settings