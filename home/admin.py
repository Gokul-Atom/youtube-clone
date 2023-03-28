from django.contrib import admin

# Register your models here.
from .models import User, Video, Channel, Comment, Tag

admin.site.register(User)
admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Tag)