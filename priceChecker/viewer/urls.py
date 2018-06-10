from django.urls import path

from . import views


app_name = 'viewer'

urlpatterns = [
    path('', views.index, name='index'),
    path('prods/', views.all_prods, name='all_prods'),
    path('inactive/', views.inactive_prods, name='inactive_prods'),
    path('prod/<int:product_id>/', views.prod, name='prod'),
    path('prod/<int:product_id>/prices/', views.prices, name='prices'),
    path('store/<int:store_id>/', views.store, name='store'),
    path('stores/', views.stores, name='stores'),
    path('sessions/', views.sessions, name='sessions'),
    path('prices_fig/<int:product_id>/', views.prices_fig, name='prices_fig'),
    # path('session/<int:session_id>/', views.session, name='session'),
]
