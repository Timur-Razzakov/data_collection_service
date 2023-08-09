from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),
    path('api/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('redoc/', TemplateView.as_view(
    #     template_name='redoc.html',
    #     extra_context={'schema_url': 'openapi-schema'}
    # ), name='redoc'),

]
