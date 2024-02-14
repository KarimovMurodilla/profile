from django.contrib import admin

from .models import CustomUser, Comment


admin.site.register(CustomUser)
admin.site.register(Comment)
