from django.contrib import admin
from .models import User, Post, Following

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active', 'date_joined')
    search_fields = ['first_name', 'last_name', 'date_joined']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')
    search_fields = ['title','date_created']

@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'following_user_id')