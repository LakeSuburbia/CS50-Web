from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import *


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def follow(request, userid):
    if request.method == "POST":
        follower = request.user
        if follower is not None:
            followee = User.objects.get(userid)

            if Follows.objects.filter(follower=follower, followee=followee).exists():
                Follows.objects.get(follower=follower, followee=followee).delete()
            else:
                Follows.objects.create(follower=follower, followee=followee)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)


def like(request, postid):
    if request.method == "POST":
        liker = request.user
        if liker is not None:
            liked = Post.objects.get(postid)

            if Likes.objects.filter(liker=liker, liked=liked).exists():
                Likes.objects.get(liker=liker, liked=liked).delete()
                return JsonResponse({"message": "Post is succesfully unliked"}, status=201)
            else:
                Follows.objects.create(liker=liker, liked=liked)
                return JsonResponse({"message": "Post is succesfully liked"}, status=201)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)


def make_post(request):
    if request.method == "POST":
        poster = request.user
        if poster is not None:
            body = request.POST["body"]
            time = datetime.now()
            Post.objects.create(poster = poster, body = body, time = time)
            
            return JsonResponse({"message": "Post is succesfully posted"}, status=201)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)


def edit_post(request, postid):
    if request.method == "POST":
        poster = request.user
        if poster is not None:
            post = Post.objects.get(postid)
            if post.poster == poster:
                post.body = request.POST["body"]
                post.save()
            return JsonResponse({"message": "Post is succesfully edited"}, status=201)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)


def get_followcount(request, userid):
    if request.method == "GET":
        user = request.user
        if user is not None:
            if User.objects.filter(id=userid).exists:
                followingcount = 0
                followercount = 0
                followingcount += Follows.objects.filter(follower=userid).count()
                followercount += Follows.objects.filter(followee=userid).count()
                return JsonResponse([{
                    "followers": followercount,
                    "following": followingcount
                }], safe=False)
            return JsonResponse({"message": "User does not exist"}, status=301)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)

def get_currentuser(request):
    if request.method == "GET":
        if request.user:
            data = {
                "username":request.user.username, 
                "userid":request.user.id
            }
            #data = serializers.serialize("json", user, fields=('username'))
            
            return JsonResponse(data)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)