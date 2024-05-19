from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import ecom_app.views
from ecom_app import views

urlpatterns = [
                  #   ADMIN URL
                  path('admin/', admin.site.urls),


                  #   APP URLS
                  path('', include('ecom_app.urls')),


                  #      libraries path
                  path('tinymce/', include('tinymce.urls')),


                  #   user Authintication
                  path('login/', views.user_login, name='handlelogin'),
                  path('signup/', views.signup, name='signup'),
                  path('',include('django.contrib.auth.urls')),


                  # profile section
                  path('user/profile/',views.profile,name='profile'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = ecom_app.views.custom_404_view
