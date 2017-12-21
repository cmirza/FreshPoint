from django.shortcuts import render
from .local_variables import goog_api_key
import requests


def index(request):
    return render(request, 'freshpoint/index.html')


def results(request):
    user_zip = request.POST['input_zip']

    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(user_zip, goog_api_key))
    api_response_dict = api_response.json()

    for i in api_response_dict['results'][0]['address_components']:
        if i['types'] == ["administrative_area_level_1", "political"]:
            user_state = i['short_name']
            user_state_verbose = api_response_dict['results'][0]['formatted_address']

    context = {'user_state_verbose': user_state_verbose, 'user_state': user_state}

    return render(request, 'freshpoint/results.html', context)
