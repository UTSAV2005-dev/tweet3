from django.contrib import admin
from .models import Tweet,Comment,Profile
# Register your models here.
admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(Profile)
