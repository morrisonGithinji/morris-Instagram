from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Stream)
admin.site.register(Likes)
admin.site.register(Follow)
admin.site.register(Comment)