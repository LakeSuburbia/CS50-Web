
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow/<int:userid>", views.follow, name="follow"),
    path("like/<int:postid>", views.like, name="like"),
    path("user/<int:userid>", views.userpage, name="userpage"),
    path("myProfile", views.my_profile, name="my_profile"),
    path("post", views.make_post, name="make_post"),
    path("posts", views.get_allposts, name="get_allposts"),
    path("posts/<int:userid>", views.get_posts, name="get_posts"),
    path("get_currentuser", views.get_currentuser, name="get_currentuser"),
    path("get_followcount/<int:userid>", views.get_followcount, name="get_followcount"),
]
