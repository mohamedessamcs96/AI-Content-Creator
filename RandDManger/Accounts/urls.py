from django.urls import path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
# from .views import PaymentAPI



# app_name="accounts"



urlpatterns=[
    path('admin/', admin.site.urls),
	path('product_page', views.product_page, name='product_page'),
    path('create_report/<str:data>/', views.create_report, name='createreport'),
	path('payment_successful', views.payment_successful, name='payment_successful'),
	path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
	path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    path('content_creator/',views.content_creator,name='contentcreator'),
    path('register/',views.register_request,name='register'),
    path('signup/',views.signup,name='signup'),
    path('admin_panel/',views.admin_panel,name='adminpanel'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('',views.home_page,name='homepage'),
    path('home_info/',views.home_info,name='homeinfo'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        

