from django.contrib import admin
from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id","title","author"]

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ["id","user","rate_number"]