import io

from django.db.models import Count
from django.http import HttpResponse  # Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

from .models import Product, Price, Store, Session


def index(request):
    active = get_list_or_404(Product.objects.select_related('store'),
                             active=1)
    context = {
        'active': active,
        'count': len(active)
    }
    return render(request, 'viewer/index.html', context)


def all_prods(request):
    active = get_list_or_404(Product.objects.select_related('store'),
                             active=1)
    inactive = get_list_or_404(Product.objects.select_related('store'),
                               active=0)
    context = {
        'active': active,
        'ac_cnt': len(active),
        'inactive': inactive,
        'in_cnt': len(inactive),
    }
    return render(request, 'viewer/all_prods.html', context)


def inactive_prods(request):
    inactive = get_list_or_404(Product.objects.select_related('store'),
                               active=0)
    context = {
        'inactive': inactive,
        'count': len(inactive),
    }
    return render(request, 'viewer/inactive_prods.html', context)


def prod(request, product_id):
    p = get_object_or_404(Product.objects.select_related('store'),
                          product_id=product_id)
    # prices = get_list_or_404(
    #     Price.objects.select_related('session').order_by('-session__date'),
    #     product_id=product_id)
    prices = Price.objects.select_related('session').filter(
        product_id=product_id
    ).order_by('-session__date')
    context = {
        'prod': p,
        'prices': prices,
        'prices_count': len(prices),
    }
    return render(request, 'viewer/prod.html', context)


def store(request, store_id):
    store = get_object_or_404(Store, store_id=store_id)
    active_prods = Product.objects.filter(store_id=store_id, active=1)
    inactive_prods = Product.objects.filter(store_id=store_id, active=0)
    context = {
        'store': store,
        'active': active_prods,
        'act_count': len(active_prods),
        'inactive': inactive_prods,
        'inact_count': len(inactive_prods),
    }
    return render(request, 'viewer/store.html', context)


def stores(request):
    stores = get_list_or_404(Store.objects.annotate(Count('product')))
    return render(request, 'viewer/stores.html', {'stores': stores})

def sessions(request):
    sessions = get_list_or_404(
        Session.objects.annotate(Count('price')).order_by('-date')
    )
    context = {
        'sessions': sessions,
        'count': len(sessions),
    }
    return render(request, 'viewer/sessions.html', context)


def prices(request, product_id):
    return HttpResponse("You're looking at prices for product %s." %
                        product_id)


def prices_fig(request, product_id):
    prices = Price.objects.select_related('session').filter(
        product_id=product_id
    ).order_by('session__date')
    d, p = [], []
    for row in prices:
        d.append(row.session.date)
        p.append(row.amount)
    buf = io.BytesIO()
    myFmt = mdates.DateFormatter('%d/%m')
    f, ax = plt.subplots()
    ax.plot(d, p)
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_title('Price graph')
    f.savefig(buf, format='png')
    plt.close(f)
    buf.seek(0)
    return HttpResponse(buf.read(), content_type='image/png')
