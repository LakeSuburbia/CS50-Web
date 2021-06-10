from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from .models import Post, User, Likes, Follows
def extend_posts(request, posts):
    user = request.user
    try:
        likes = Likes.objects.filter(liker = user)
    except:
        likes = []
    for post in posts:
        post.liked = False
        for like in likes:
            if post == like.liked:
                post.liked = True
    return posts

def render_posts(request, posts, frontpage):
    page = paginate_posts(request, posts)

    return render(request, "network/index.html", {
        'posts': page,
        'frontpage': frontpage,
        })

def paginate_posts(request, posts):
    posts = extend_posts(request, posts)
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return page

def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render_posts(request, posts, True)


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
        followee = User.objects.get(id=userid)

        if Follows.objects.filter(follower=follower, followee=followee).exists():
            Follows.objects.get(follower=follower, followee=followee).delete()
        else:
            Follows.objects.create(follower=follower, followee=followee)
    return userpage(request, userid)

def like(request, postid):
    if request.method == "GET":
        liker = request.user
        if liker is not None:
            liked = Post.objects.get(id = postid)
            is_liked = False

            if Likes.objects.filter(liker=liker, liked=liked).exists():
                Likes.objects.get(liker=liker, liked=liked).delete()
                liked.like -= 1
                liked.save()

            else:
                Likes.objects.create(liker=liker, liked=liked)
                liked.like += 1
                liked.save()
                is_liked=True

            data = {
                "likes": liked.like,
                "is_liked": is_liked,
            }
            
            return JsonResponse(data)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)

def edit(request, postid):
    if request.method == "POST":
        liker = request.user
        if liker is not None:
            liked = Post.objects.get(postid)

            if Likes.objects.filter(liker=liker, liked=liked).exists():
                Likes.objects.get(liker=liker, liked=liked).delete()
                liked.like -= 1
                return JsonResponse({"message": "Post is succesfully unliked"}, status=201)
            else:
                Follows.objects.create(liker=liker, liked=liked)
                liked.like += 1
                return JsonResponse({"message": "Post is succesfully liked"}, status=201)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)


def make_post(request):
    if request.method == "POST":
        poster = request.user
        if poster is not None:
            body = request.POST["body"]
            Post.objects.create(poster = poster, body = body)
            
            return index(request)
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




def get_currentuser(request):
    if request.method == "GET":
        if request.user:
            data = {
                "username":request.user.username, 
                "userid":request.user.id
            }
            return JsonResponse(data)
        return JsonResponse({"message": "User is not authorized"}, status=301)
    return JsonResponse({"message": "Wrong request"}, status=500)



def userpage(request, userid):
    user = User.objects.get(id = userid)
    posts = Post.objects.filter(poster = userid)
    posts = paginate_posts(request, posts)
    followingcount = 0
    followercount = 0
    following = Follows.objects.filter(follower=userid)
    followingcount += following.count()

    followers = Follows.objects.filter(followee=userid)
    followercount += followers.count()

    follows = 0
    if followers.filter(follower = request.user).exists():
        follows = 1
    return render(request, "network/profile.html", {
        'username': user.username,
        'userid': userid,
        'followers': followercount,
        'following': followingcount,
        'posts': posts,
        'follows': follows
        })

def following(request):
    followquery = Follows.objects.filter(follower=request.user.id)
    followlist = [followee.followee.id for followee in followquery]
    posts = Post.objects.filter(poster__in=followlist).order_by('-timestamp')
    return render_posts(request, posts, True)