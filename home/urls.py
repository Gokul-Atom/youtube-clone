from django.urls import path
from . import views


urlpatterns = [
    path('load/', views.loadingScreen, name='loading-screen'),
    path('', views.home, name='home'),
    path('video/<str:pk>/', views.videoPlayer, name='video-player'),
    
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('check-username/', views.checkUsername, name='check-username'),
    path('logout/', views.logoutUser, name='logout'),
    path('reset-password/', views.forgetPassword, name='reset-password'),
    path('change-password/', views.generateResetLink, name='change-password'),

    path('update-profile/', views.updateProfile, name='update-profile'),
    path('delete-profile/', views.deleteProfile, name='delete-profile'),
    path('profile/', views.profilePage, name='profile'),
    
    path('toggle-incognito-mode/', views.toggleIncognitoMode, name='toggle-incognito-mode'),

    path('update-channel/<str:channel_id>/', views.updateChannel, name='update-channel'),
    path('create-channel/', views.createChannel, name='create-channel'),
    path('check-handle/', views.checkHandle, name='check-handle'),
    path('channel/<str:pk>/', views.channelPage, name='channel-page'),
    
    path('my-library/', views.libraryPage, name='library'),
    
    path('subscribe/<str:channel_id>/', views.subscribeChannel, name='subscribe'),
    path('unsubscribe/<str:channel_id>/', views.unsubscribeChannel, name='unsubscribe'),
    path('like/<str:video_id>/', views.likeVideo, name='like'),
    path('dislike/<str:video_id>/', views.dislikeVideo, name='dislike'),
    path('edit-comment/<str:video_id>/<str:comment_id>/', views.editComment, name='edit-comment'),
    path('delete-comment/<str:video_id>/<str:comment_id>/', views.deleteComment, name='delete-comment'),
    
    path('delete/<str:channel_id>/', views.deleteChannel, name='delete-channel'),

    path('video-upload/<str:channel_id>/', views.videoUpload, name='video-upload'),
    path('edit-video/<str:video_id>/', views.editVideo, name='edit-video'),
    path('delete-video/<str:video_id>/', views.deleteVideo, name='delete-video'),
]
