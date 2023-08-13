from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('posts/<slug>/', views.posts, name='posts'),
    path('post/<slug>/', views.post, name='post'),
    path("createpost", views.createpost, name = "createpost"),
]
