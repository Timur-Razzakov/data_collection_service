from django.urls import path
from .views import *
# app_name = 'accounts'
urlpatterns = [
    path('registration/', register_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('update/', update_view, name='update'),
    path('delete/', delete_view, name='delete_user'),
    # path('contact/', contact_view, name='contact'),

]
