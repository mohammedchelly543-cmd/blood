from django.contrib import admin
from django.urls import path, include
from accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acc_views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('donations/', include('donations.urls')),
    path('campaigns/', include('campaigns.urls')),
]