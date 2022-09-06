
from django.urls import path

from . import views


app_name = 'network'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.create_post, name="new-post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    #API routes
    path("follow/<str:username>", views.follow, name="follow"),
    path("post/<str:username>/<int:post_id>", views.post, name="post"),
]
