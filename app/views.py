"""
    Views to access microsoft graph api for user details.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests

def get_graph_token():
    """ Get graph token from AAD url """
    try:
        url = settings.AD_URL

        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}

        data = {
            'grant_type': 'client_credentials',
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'scope': 'https://graph.microsoft.com/.default'
        }
        response = requests.post(url=url, headers=headers, data=data)
        json_response = response.json()
        return json_response
        
    except:
        return None

def login_successful(request):
    """ Get user details from microsoft graph apis """
    graph_token = get_graph_token()
    print("access_token (for inspection):", graph_token.get('access_token'))
    try:
        if graph_token:
            url = 'https://graph.microsoft.com/v1.0/users/' + request.user.username
            headers = {
                'Authorization': 'Bearer ' + graph_token['access_token'],
                'Content-Type': 'application/json',
            }
            response = requests.get(url=url, headers=headers)
            json_response = response.json()

            print("json_response: ", json_response)
            return HttpResponse(f"Hi {json_response['givenName']}, Login successful")
    except:
        return HttpResponse("Unable to fetch user details from graph APIs")
