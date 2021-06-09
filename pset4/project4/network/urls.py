
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow/<int:userid>", views.follow, name="follow"),
    path("like/<int:postid>", views.like, name="like"),
    path("user/<int:userid>", views.userpage, name="user"),
    path("post", views.make_post, name="make_post"),
    path("following", views.following, name="following"),
    path("get_currentuser", views.get_currentuser, name="get_currentuser"),
]
