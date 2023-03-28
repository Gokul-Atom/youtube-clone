from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(null=True, max_length=200, unique=False)
    email = models.EmailField(null=True, unique=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    incognito_mode = models.BooleanField(default=False)

    subscriptions = models.ManyToManyField('Channel', related_name='subscriptions')
    
    likes = models.ManyToManyField('Video', related_name='likes')
    dislikes = models.ManyToManyField('Video', related_name='dislikes')

    otp = models.CharField(max_length=10, null=True, blank=True)
    password_reset_request_time = models.DateTimeField(null=True, blank=True)
    password_expiry_time = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Notifications(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    
    uploaded_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_time']


class Library(models.Model):
    watched_by = models.ForeignKey('User', on_delete=models.CASCADE)
    watched = models.ManyToManyField('Video', related_name='watched')

    watched_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-watched_time']

    
    def __str__(self):
        return str(self.watched.all()[0])


class Video(models.Model):
    user_response = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(null=True, blank=True, default='video-thumbnail.png')
    video_url = models.URLField()
    channel_name = models.ForeignKey('Channel', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='tags')

    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    commentable = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return self.title


class Channel(models.Model):
    channel_admin = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    handle = models.CharField(max_length=200, unique=True)
    cover_photo = models.ImageField(null=True, blank=True, default='channel-cover-photo.png')
    logo = models.ImageField(null=True, blank=True, default='channel-thumbnail.png')
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    whatsapp = models.CharField(max_length=25, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    total_views = models.IntegerField(null=True, default=0)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name


class Comment(models.Model):
    video_comments = models.ForeignKey('Video', on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    commented_by = models.ForeignKey('User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.comments


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag
