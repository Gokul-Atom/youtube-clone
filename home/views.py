from django.shortcuts import render, redirect
from .models import Tag, Video, Channel, User, Comment, Library, Notifications
from .forms import VideoUploadForm, UserForm, CommentForm, CreateChannelForm, UpdateChannelForm, UpdateUserForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import os
import json
import random
from datetime import datetime, timedelta
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

FROM_EMAIL = os.environ.get('FROM_EMAIL')
PASSWORD = os.environ.get('PASSWORD')
first_run = True


def generateOTP(email):
    str_number = str(random.random()).split('.')[-1][-6:]
    OTP = f'{int(str_number):06d}'
    user = User.objects.get(email=email)
    user.otp = OTP
    user.password_reset_request_time = datetime.now()
    user.password_expiry_time = datetime.now() + timedelta(minutes=30)
    user.save()
    sendMail(user)


def sendMail(user):
    msg = MIMEMultipart('alternative')

    with open('home/templates/home/email-template.html') as file:
        html = file.read().replace('USERNAME', user.username).replace('OTP_PIN', user.otp).replace('THIS_YEAR', str(datetime.now().year))
        reset_msg_html = MIMEText(html, 'html')
        
    reset_msg_text = MIMEText(f'''
Hello {user.username}, you have made a request for password reset.


Enter the OTP to create new password. This OTP is valid for only 30 minutes.

{user.otp}
    ''', 'plain')

    msg['From'] = formataddr(('Tube by Gokul', FROM_EMAIL))
    msg['To'] = user.email
    msg['Subject'] = 'Password Reset'
    msg.attach(reset_msg_html)
    msg.attach(reset_msg_text)
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(FROM_EMAIL, PASSWORD)
        connection.sendmail(FROM_EMAIL, user.email, msg=msg.as_string().encode('utf-8'))


def addToLibrary(request, video):
    if request.user.is_authenticated and not request.user.incognito_mode:
        library = request.user.library_set.all()

        if library:
            for watched_video in library:
                if watched_video.watched.all():
                    if watched_video.watched.all()[0].id == video.id: # checks the watched video id from library with current video id
                        current = Library.objects.get(id=watched_video.id)
                        current.watched.add(video)
                        current.save()
                        return

        library = Library.objects.create(
            watched_by = request.user,
        )
        library.watched.add(video)
        library.save()


def getVideosFromLibrary(request):
    library = request.user.library_set.all()

    if library:
        return [video.watched.all()[0] for video in library if video.watched.all()]
    else:
        return None


def cleanVideoUploadForm(request):
    temp_form = request.POST.copy()
    temp_form['tags'] = None
    tags_id = []
    tags = request.POST.getlist('tags')

    if tags:
        if type(tags) == 'str':
            t, created = Tag.objects.get_or_create(tag=tags.strip())
            tags_id.append(t.id)
            temp_form['tags'] = t.id
        else:
            first = True
            for tag in tags:
                t, created = Tag.objects.get_or_create(tag=tag.strip())
                tags_id.append(t.id)
                if first:
                    temp_form['tags'] = t.id
                else:
                    temp_form.update({'tags': t.id})
                
    return [tags_id, VideoUploadForm(temp_form)]


def getVideoTags(object):
    tags = [tag.tag for tag in object.tags.all()]
    return tags


def updateVideoTags(request, video):
    video_tags = request.POST.get('video-tags')[:-1].lower().split(";")
    video_ids = []
    for tag in video_tags:
        cleaned_tag = tag.strip()
        if cleaned_tag:
            tags, created = Tag.objects.get_or_create(tag=cleaned_tag)
            video_ids.append(tags.id)
    video.tags.set(video_ids)


def getCommentContext(video_id):
    video = Video.objects.get(id=video_id)
    comments = video.comment_set.all()
    context = {
        'comments': comments,
        'this_video': video,
        'count': comments.count(),
    }
    return context


def createNotification(video_id, channel_id):
    channel = Channel.objects.get(id=channel_id)
    video = Video.objects.get(id=video_id)
    subscribers = channel.subscriptions.all()

    for subscriber in subscribers:
        notification = Notifications.objects.create(
            video = video,
            user = subscriber,
        )
        notification.save()


# Create your views here.
def checkUsername(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            return HttpResponse("true")
        except:
            return HttpResponse("false")


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()

            login(request, user)
            return HttpResponse(redirect('home').url)
        
        else:
            return HttpResponse(json.dumps(form.errors))

    context = {
        'form': form,
        'page': 'register',
    }
    return render(request, 'home/login_register.html', context)


def generateResetLink(request):
    global first_run
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        form = PasswordResetForm(request.POST, instance=user)
        otp = request.POST.get('otp')
        if otp:
            if user.password_expiry_time.replace(tzinfo=None) < datetime.now():
                data = {'otp': ['OTP expired!']}
                return HttpResponse(json.dumps(data))
            
            if user.otp != otp:
                data = {'otp': ['OTP incorrect!']}
                return HttpResponse(json.dumps(data))
        
            else:
                if form.is_valid():
                    user.set_password(request.POST.get('password1'))
                    user.save()
                    messages.success(request, 'Password changed succesfully.')
                    return HttpResponse(redirect(home).url)
                else:
                    return HttpResponse(json.dumps(form.errors))
        else:
            if first_run:
                first_run = False
                generateOTP(email)
                data = {'otp': []}
                return HttpResponse(json.dumps(data))
            else:
                data = {'otp': ['OTP cannot be empty.']}
                return HttpResponse(json.dumps(data))


def forgetPassword(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    global first_run
    form = PasswordResetForm()
    if request.GET.get('csrfmiddlewaretoken'):
        email = request.GET.get('email')
        try:
            first_run = True
            user = User.objects.get(email=email)
            return HttpResponse('true')
        except:
            return HttpResponse('false')
    
    context = {
        'form': form,
        'page': 'password-reset',
    }
    return render(request, 'home/login_register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User doesn't exists.")
            return redirect('login')
        
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong password!')
        
    context = {
        'page': 'login',
    }
    return render(request, 'home/login_register.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profilePage(request):
    channels = request.user.channel_set.all()
    library = getVideosFromLibrary(request)

    context = {
        'channels': channels,
        'videos': library,
    }
    return render(request, 'home/profile-page.html', context)


@login_required(login_url='login')
def updateProfile(request):
    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors)

        return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'home/update-profile.html', context)


@login_required(login_url='login')
def deleteProfile(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')


@login_required(login_url='login')
def createChannel(request):
    form = CreateChannelForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = CreateChannelForm(request.POST)
        if form.is_valid():
            cover_photo = request.FILES.get('cover_photo')
            logo = request.FILES.get('logo')
            channel = Channel.objects.create(
                channel_admin=request.user,
                name=request.POST.get('name'),
                handle=request.POST.get('handle'),
                description=request.POST.get('description'),
                location=request.POST.get('location'),
                website = request.POST.get('website'),
                facebook = request.POST.get('facebook'),
                instagram = request.POST.get('instagram'),
                twitter = request.POST.get('twitter'),
                whatsapp = request.POST.get('whatsapp'),
            )
            if cover_photo:
                channel.cover_photo = cover_photo
            if logo:
                channel.logo = logo
            channel_id = channel.id
            channel.save()
            return HttpResponse(redirect('channel-page', channel_id).url)
        else:
            return HttpResponse(json.dumps(form.errors))
            
    return render(request, 'home/create-update-channel.html', context)


def checkHandle(request):
    channels = Channel.objects.all()
    if request.method == 'POST':
        handle = request.POST.get('handle')
        for channel in channels:
            if channel.handle == handle:
                return HttpResponse("true")
        return HttpResponse("false")


@login_required(login_url='login')
def updateChannel(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    form = UpdateChannelForm(instance=channel)

    if request.method == 'POST':
        form = UpdateChannelForm(request.POST, instance=channel)
        logo = request.FILES.get('logo')
        cover_photo = request.FILES.get('cover_photo')
        if form.is_valid():
            update_channel = form.save(commit=False)
            if logo:
                update_channel.logo = logo
            if cover_photo:
                update_channel.cover_photo = cover_photo
            update_channel.save()
            return HttpResponse(redirect('channel-page', channel_id).url)
        else:
            return HttpResponse(json.dumps(form.errors))

    context = {
        'form': form,
        'channel': channel,
    }
    return render(request, 'home/create-update-channel.html', context)


def loadingScreen(request):
    return render(request, 'home/loading-screen.html')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    tag = request.GET.get('tag') if request.GET.get('tag') else ''

    tags = Tag.objects.all()

    videos = Video.objects.filter(
        Q(title__icontains=q) |
        Q(channel_name__name__icontains=q) |
        Q(tags__tag__icontains=q)
    )
    if tag:
        videos = Video.objects.filter(
            Q(tags__tag__icontains=tag)
        )
    context = {
        'videos': videos.distinct(),
        'tags': tags,
    }

    return render(request, 'home/home.html', context)


def videoPlayer(request, pk):
    video = Video.objects.get(id=pk)
    video.views += 1
    video.channel_name.total_views += 1

    addToLibrary(request, video)

    video.save()
    video.channel_name.save()

    tags = getVideoTags(video)
    related_videos = []
    for tag in tags:
        related_videos.append(Video.objects.filter(
            Q(tags__tag__icontains=tag)
        ))

    unique_videos = Video.objects.none()
    for vid in related_videos:
        unique_videos |= vid

    if request.method == 'POST':
        Comment.objects.create(
            video_comments=video,
            comments=request.POST.get('comment'),
            commented_by=request.user,
        )

        context = getCommentContext(pk)
        return render(request, 'home/comments.html', context)

    comments = video.comment_set.all()
    context = {
        'tags': tags,
        'videos': unique_videos.distinct(),
        'this_video': video,
        'video_url': video.video_url.replace('youtu.be', 'youtube.com/embed'),
        'form': CommentForm(),
        'comments': comments,
        'count': comments.count(),
        'subscribed': True if request.user.is_authenticated and video.channel_name in request.user.subscriptions.all() else False,
        'liked': True if request.user.is_authenticated and video in request.user.likes.all() else False,
        'disliked': True if request.user.is_authenticated and video in request.user.dislikes.all() else False,
    }

    return render(request, 'home/player.html', context)


@login_required(login_url='login')
def editComment(request, video_id, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id=comment_id)
        comment.comments = request.POST.get('comment')
        comment.save()
        context = getCommentContext(video_id)
        return render(request, 'home/comments.html', context)


@login_required(login_url='login')
def deleteComment(request, video_id, comment_id):
    if request.method == "DELETE":
        Comment.objects.get(id=comment_id).delete()
        context = getCommentContext(video_id)
        return render(request, 'home/comments.html', context)


@login_required(login_url='login')
def videoUpload(request, channel_id):
    form = VideoUploadForm()

    if request.method == 'POST':
        channel = Channel.objects.get(id=channel_id)
        thumbnail = request.FILES.get('thumbnail')
                
        tags_id ,form = cleanVideoUploadForm(request)

        if form.is_valid():
            video = Video.objects.create(
                title=request.POST.get('title'),
                video_url=request.POST.get('video_url'),
                channel_name=channel,
                description=request.POST.get('description'),
                commentable=True if request.POST.get('commentable') else False,
            )

            if thumbnail:
                video.thumbnail = thumbnail
            
            video.tags.set(tags_id)
            video.save()

            createNotification(video.id, channel_id)
            
            return HttpResponse(redirect('home').url)
        
        else:
            return HttpResponse(json.dumps(form.errors))
        
    context = {
        'form': form,
        'tags': Tag.objects.all(),
    }
    return render(request, 'home/video-upload.html', context)


@login_required(login_url='login')
def editVideo(request, video_id):
    video = Video.objects.get(id=video_id)
    form = VideoUploadForm(instance=video)

    if request.method == "POST":
        thumbnail = request.FILES.get('thumbnail')
        
        if thumbnail:            
            video.thumbnail = thumbnail

        tags_id, form = cleanVideoUploadForm(request)
        if form.is_valid():
            video.title = request.POST.get('title')
            video.video_url = request.POST.get('video_url')
            video.description = request.POST.get('description')
            video.commentable = True if request.POST.get('commentable') else False
            video.tags.set(tags_id)
            
            video.save()
            return HttpResponse(redirect('video-player', video_id).url)
        else:
            return HttpResponse(json.dumps(form.errors))
    
    context = {
        'form': form,
        'tags': Tag.objects.all(),
        'video': video,
        'video_tags': json.dumps(getVideoTags(video)),
    }

    return render(request, 'home/video-upload.html', context)


@login_required(login_url='login')
def deleteVideo(request, video_id):
    channel_id = Video.objects.get(id=video_id).channel_name.id
    Video.objects.get(id=video_id).delete()
    return redirect('channel-page', channel_id)


@login_required(login_url='login')
def subscribeChannel(request, channel_id):
    if request.method == 'POST':
        channel = Channel.objects.get(id=channel_id)
        request.user.subscriptions.add(channel)
        subs_count = channel.subscriptions.count()
        return HttpResponse(subs_count)


@login_required(login_url='login')
def unsubscribeChannel(request, channel_id):
    if request.method == 'POST':
        channel = Channel.objects.get(id=channel_id)
        request.user.subscriptions.remove(channel)
        subs_count = channel.subscriptions.count()
        return HttpResponse(subs_count)


@login_required(login_url='login')
def likeVideo(request, video_id):
    if request.method == 'POST':
        video = Video.objects.get(id=video_id)

        request.user.likes.add(video)
        request.user.dislikes.remove(video)

        context = {
            'likes': video.likes.count(),
            'dislikes': video.dislikes.count(),
        }
        return HttpResponse(json.dumps(context))


@login_required(login_url='login')
def dislikeVideo(request, video_id):
    if request.method == 'POST':
        video = Video.objects.get(id=video_id)

        request.user.likes.remove(video)
        request.user.dislikes.add(video)

        context = {
            'likes': video.likes.count(),
            'dislikes': video.dislikes.count(),
        }

        return HttpResponse(json.dumps(context))


@login_required(login_url='login')
def toggleIncognitoMode(request):
    if request.user.incognito_mode:
        request.user.incognito_mode = False
    else:
        request.user.incognito_mode = True
    
    request.user.save()
    return redirect('home')


def channelPage(request, pk):
    channel = Channel.objects.get(id=pk)
    videos = channel.video_set.all()
    other_channels = channel.channel_admin.channel_set.all()

    context = {
        'channel': channel,
        'videos': videos,
        'other_channels': other_channels,
        'subscribed': True if request.user.is_authenticated and channel in request.user.subscriptions.all() else False,
    }
    return render(request, 'home/channel-page.html', context)


@login_required(login_url='login')
def deleteChannel(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    channel.delete()
    return redirect('profile')


@login_required(login_url='login')
def libraryPage(request):
    videos = getVideosFromLibrary(request)
    context = {
        'videos': videos,
    }

    return render(request, 'home/library-page.html', context)
