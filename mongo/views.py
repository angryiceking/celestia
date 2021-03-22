from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from pymongo import MongoClient
from bson.son import SON
from .utils import manual_process

import datetime, json
# Create your views here.

client = MongoClient('mongodb://guest:Z8zDntK3aC0l@54.251.133.139:27017/?authSource=logs_db')

class MongoView(View):

    def get(self, request):
        data = manual_process()
        return render(request, 'index.html', {"data": data})

    def post(self, request):
        data = manual_process()
        context = {
            "series": [],
            "success": [],
            "error": []
        }
        for k, v in data.items():
            context['series'].append(k)
            context['success'].append(v['success'])
            context['error'].append(v['error'])

        return HttpResponse(json.dumps(context), status=200)

    def transform_date(self, date):
        try:
            ndate = datetime.datetime.strftime(date, '%Y-%m-%d %X')
        except ValueError:
            ndate = datetime.datetime.strftime(date, '%Y-%m-%d %X')

        return ndate