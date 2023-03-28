from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Video, Channel, User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'avatar', 'password1', 'password2']


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']


class PasswordResetForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'otp', 'password1', 'password2']
        # exclude = ['username', 'name', 'date_joined', 'subscriptions', 'likes', 'dislikes']


class CreateChannelForm(ModelForm):
    class Meta:
        model = Channel
        fields = '__all__'
        exclude = ['channel_admin', 'subscribers', 'created', 'total_views']


class UpdateChannelForm(ModelForm):
    class Meta:
        model = Channel
        fields = '__all__'
        exclude = ['channel_admin', 'handle', 'subscribers', 'created', 'total_views']


class VideoUploadForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'thumbnail', 'video_url', 'description', 'tags', 'commentable']

        def __init__(self, *args, **kwargs):
            super(VideoUploadForm).__init__(*args, **kwargs)
            self.fields['tags'].required = False


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
