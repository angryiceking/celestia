from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .utils import process_query

import datetime, json
# Create your views here.

class MongoView(View):

    def get(self, request, interval):
        data = process_query(interval)
        return render(request, 'index.html', {"data": data, "minute": interval})

    def post(self, request, interval):
        data = process_query(interval)
        context = {
            "series": [],
            "success": [],
            "error": [],
        }
        # print(data)
        for k, v in data.items():
            context['series'].append(k)
            context['success'].append(v['success'])
            context['error'].append(v['error'])

        return HttpResponse(json.dumps(context), status=200)
