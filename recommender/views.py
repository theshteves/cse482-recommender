import json
import os
import pprint

from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import forms
from .nick import nmfalgo as nick_algo, asin_lookup as nick_al
from .steven import get_products as steven_gp

DATAFILE = os.path.join(os.path.dirname(__file__), 'nick', 'output.csv')


def _HttpJson(dictionary):
    '''Construct HTTP Response in JSON from dictionary'''

    response_json = json.dumps(dictionary, indent=4)
    return HttpResponse(response_json, content_type='application/json')


def index(request):
    form = forms.UserForm()

    if request.method == 'POST':
        form = forms.UserForm(request.POST)

        if form.is_valid():
            return redirect('/recommend?user={}'.format(form.cleaned_data['username']))

    return render(request, 'login.html', locals())


def recommend(request):
    form = forms.RecommendForm()
    user = request.GET.get('user', 'guest')
    #TODO: introduce more products in case nick can't find them
    products = steven_gp.get_products(datafile=DATAFILE)
    products = nick_al.asin_lookup(products)
    pprint.pprint(locals())

    if request.method == 'POST':
        form = forms.RecommendForm(request.POST)

        if form.is_valid():
            return render(request, 'results.html', locals())

    return render(request, 'recommend.html', locals())


def compute(request):

    # Compute NMF
    review_data = [['user', asin, rating] for asin, rating in request.GET.items()]
    results = nick_algo.run_NMF(review_data, 'user', 3)

    asins = [item[1] for item in results]
    names = nick_al.asin_lookup(asins)
    """Sample data for dev purposes
    names = [
        ['B00JE1KOWA',
            'http://ecx.images-amazon.com/images/I/511qsJyEnZL._SY300_.jpg',
            'RCA RACE8002E Energy Star 8000 BTU Window Air Conditioner with Remote Control 115-volt'],
        ['B00GYJZER0',
            'http://ecx.images-amazon.com/images/I/31VhzV3qzmL._SY300_.jpg',
            'Stainless Steel - Hot or Cold Drink Tumbler - Double Wall Insulated with Silicone Sip Lid - 16oz.'],
        ['B00GX0DN7I',
            'http://ecx.images-amazon.com/images/I/41o0gt2yRoL._SX300_.jpg',
            'ThriftyVac Food Vacuum Packing System']
    ]
    """

    response = {}
    for i, (asin, img, name) in enumerate(names, start=1):
        response[f'name{i}'] = name
        response[f'img{i}'] = img

    return _HttpJson(response)

