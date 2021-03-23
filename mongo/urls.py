from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'mongo'
urlpatterns = [
    path('', MongoView.as_view(), {'interval': 5}, name='view'),
    path('<int:interval>', csrf_exempt(MongoView.as_view()), name='view'),
]
