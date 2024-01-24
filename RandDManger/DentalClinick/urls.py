"""Archives URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import handler404
from DentalClinick import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

handler404 = 'Accounts.views.custom_404_view'
handler500 = 'Accounts.views.custom_500_view'

def default_home(request):
    return redirect('ar/')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',default_home),
    path('en/', include(('Accounts.urls'))),
    path('ar/', include(('Accounts.urls')))
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
