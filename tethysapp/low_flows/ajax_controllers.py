from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def bar(request):
    """
    Controller for the app home page.
    """
    feature_id = None

    if request.GET and 'feature_id' in request.GET:
        feature_id = request.GET.get('feature_id')

    # Define data dictionary
    json_dict = {}
    print(json_dict)

    # Add feature_id property to data dictionary
    if feature_id:
        json_dict['feature_id'] = feature_id

    print(feature_id)

    return JsonResponse(json_dict)
