# urls.py
from django.urls import path
from . import views
# from .views import  comment_success_view
from .views import search
from .views import register_view
from .views import link_success_view


urlpatterns = [
    # path('/', views.index, name='index'),
    path('<int:news_id>/', views.detail, name='news_detail'),
    path('<int:news_id>/vote/', views.vote, name='vote'),
    path('search/', search, name='search'),
    # path('vote', views.vote, name='vote'),
    path('/', views.news_list, name='news_list'),
    # Auth Urls
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # path('comment/', views.comments_view, name='comment_form'),
    path('comments/', views.comments_view, name='comments_view'),
    path('submit_link/', views.submit_link, name='submit_link'),


    # path('comment/success/', comment_success_view, name='comment_success'),
    path('link/success/', link_success_view, name='link_success'),


    path('links/', views.link_submission_list, name='link_submission_list'),



    

]



