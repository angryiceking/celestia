from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'mongo'
urlpatterns = [
    path('', csrf_exempt(MongoView.as_view()), name='view'),
]