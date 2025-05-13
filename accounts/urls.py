from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('history/', views.watch_history, name='watch_history'),
] 