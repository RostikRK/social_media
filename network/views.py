import json
import operator

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User, Post, Following


def index(request):
    post_list = Post.objects.all().order_by("-date_created")
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("network:index")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect("network:index")


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
        return redirect("network:index")
    else:
        return render(request, "network/register.html")


@login_required
def following(request):
    followings = Following.objects.filter(user_id=request.user)
    post_list = []
    for account in followings:
        user_post_list = Post.objects.filter(creator=account.following_user_id)
        post_list.extend(user_post_list)
    post_list.sort(key=operator.attrgetter('date_created'), reverse=True)
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "network/index.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        post = Post.objects.create(creator=request.user, title=title, content=content)
        post.save()
        return redirect("network:index")
    else:
        return render(request, "network/new-post.html")

def profile(request, username):
    post_list = Post.objects.filter(creator=User.objects.get(username=username)).order_by("-date_created")
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    context["post_amount"] = Post.objects.filter(creator=User.objects.get(username=username)).count()
    context["followers"] = Following.objects.filter(following_user_id=User.objects.get(username=username)).count()
    context["following"] = Following.objects.filter(user_id=User.objects.get(username=username)).count()
    context["username"] = username;
    return render(request, "network/profile.html", context)

@login_required
@csrf_exempt
def follow(request, username):
    if request.method == "GET":
        try:
            follow = Following.objects.get(user_id=request.user, following_user_id=User.objects.get(username=username))
            return JsonResponse({"follows": "True"}, status=200)
        except Following.DoesNotExist:
            return JsonResponse({"follows": "False"}, status=200)
    elif request.method == "PUT":
        try:
            follow = Following.objects.get(user_id=request.user, following_user_id=User.objects.get(username=username))
            follow.delete()
            return JsonResponse({"follows": "False"}, status=200)
        except Following.DoesNotExist:
            follow = Following.objects.create(user_id=request.user, following_user_id=User.objects.get(username=username))
            follow.save()
            return JsonResponse({"follows": "True"}, status=200)

@login_required
@csrf_exempt
def post(request, post_id, username):
    print(username)
    post = Post.objects.get(pk=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "PUT" and username == post.creator.username:
        data = json.loads(request.body)
        print(data)
        if data.get("new_content") is not None:
            post.content = data["new_content"]
        if data.get("liked_action") is not None:
            if data.get("liked_action") == "Add":
                post.likes.add(User.objects.get(username=request.user))
            else:
                post.likes.remove(User.objects.get(username=request.user))
        post.save()
        return JsonResponse({
            "success": "Updated"
        }, status=204)
    elif request.method == "PUT" and username == post.creator.username:
        return JsonResponse({
            "error": "You are not the owner of the post"
        }, status=400)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)