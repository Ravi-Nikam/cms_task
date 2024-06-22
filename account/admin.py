from typing import Any
from django.contrib import admin
from .models import CustomUser, Post, Like
from django.contrib.auth.hashers import make_password


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'name']
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'email')

class postAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    readonly_fields = ('creation_date', 'updation_date')
    search_fields = ('title',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post,postAdmin)
admin.site.register(Like,LikeAdmin)
