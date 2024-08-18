from django.contrib import admin
from django.urls import path, include
from news.views import index,news_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL redirects to index view
    path('', news_list, name='index'),

    # News app URLs
    path('news/', include('news.urls')),

     

]
