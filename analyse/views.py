from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function

import json
import re

from django.http import JsonResponse
from django.shortcuts import render

from .forms import ScrapeForm
from .models import Amazon_Analyse


# Create your views here.

def analyse_data(request):
    if request.method == 'GET':
        print("analyse : get function")
        q = Amazon_Analyse()
        total_count, score, data, comments = q.analyse_class()

        with open('amazon_data.json') as data_file:
            f = json.load(data_file)

        title = f['name']

        # getting image data
        imageFile = open("imageData.txt")
        base64 = imageFile.readline()
        base64 = base64[3:]
        form = ScrapeForm()
        specs_list = []
        p = []
        f = open('specs.txt')
        for line in f:
            p.append(re.findall(r'"(.*?)"', line))
        # print p
        try:
            for i in xrange(0, len(p), 2):
                specs_list.append((p[i][0], p[i + 1][0]))

            print(specs_list)
        except Exception:
            pass

        return render(request, 'result.html',
                      {'data': data,
                       'comments': json.dumps(comments),
                       'title': title,
                       'image': base64,
                       'form': form,
                       'specs_list': specs_list,
                       'total_reviews': total_count,
                       'score': score}
                      )


def analyse_data_list_all(request):
    if request.method == 'GET':
        q = Amazon_Analyse()
        score, data, comments = q.analyse_class()
        return render(request, 'index.html', {'data': data, 'score': score})


def analyse_newspec(request):
    if request.method == 'POST' and request.is_ajax:
        form = ScrapeForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        # name_obj = Amazon_Url.objects.create(url=form.cleaned_data['url'] )
        spec = form.cleaned_data['spec']
        print(spec)
        qq = Amazon_Analyse()
        value, comments = qq.Amazon_spec(spec)
        # print 'Url is', url
        print('value is', value)
        print(comments)
        data = json.dumps({
            'heading': spec,
            'value': value,
            'comments_spec': comments,
        })
        return JsonResponse(data, safe=False)
        print('not sent')
