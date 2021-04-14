
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow/<int:userid>", views.follow, name="follow"),
    path("like/<int:postid>", views.like, name="like"),
    path("post", views.make_post, name="make_post"),
    path("get_currentuser", views.get_currentuser, name="get_currentuser"),
    path("get_followcount/<int:userid>", views.get_followcount, name="get_followcount"),
]
