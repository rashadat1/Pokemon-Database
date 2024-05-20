from django.shortcuts import render
from django.http import HttpResponse
# contains Python functions called view functions that handle HTTP requests and return
# HTTP responses

# Create your views here.
def index(request):
    return HttpResponse('Welcome to the Pokemon Database!')

# to call the view we need to map it to a URL which requires a URLconf
# to do this we create a urls.py file in our app directory

# process incoming HTTP requests and generate appropriate HTTP responses
# each view corresponds to a particular URL pattern

# based on the request data the view function can perform tasks such as querying a database,
# processing form submissions etc.

# after processing the HTTP request, the view function returns an HTTP response to be provided
# to the client - HTML page, JSON data, file download or whatever

# in urls.py we do the crucial step of URL routing - URL patterns that map to specific view
# functions