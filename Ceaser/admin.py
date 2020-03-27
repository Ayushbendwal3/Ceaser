from django.contrib import admin
from .models import Document, UserProfileInfo

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Document)