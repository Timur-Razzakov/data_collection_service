from django.urls import path


from .views import *

# app_name = 'scraping'
urlpatterns = [
    path('', home_view, name='home'),
    path('vacant_list/', list_view, name='vacant_list'),

]
