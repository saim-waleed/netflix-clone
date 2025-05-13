from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from main.models import UserProfile, Movie, Episode

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.userprofile
    watchlist = profile.watchlist.all()
    watched_movies = profile.watched_movies.all()
    watched_episodes = profile.watched_episodes.all()
    
    context = {
        'profile': profile,
        'watchlist': watchlist,
        'watched_movies': watched_movies,
        'watched_episodes': watched_episodes,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    
    if request.method == 'POST':
        # Update profile picture
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        # Update other profile fields if needed
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

@login_required
def watchlist(request):
    profile = request.user.userprofile
    movies = profile.watchlist.all()
    return render(request, 'accounts/watchlist.html', {'movies': movies})

@login_required
def watch_history(request):
    profile = request.user.userprofile
    watched_movies = profile.watched_movies.all()
    watched_episodes = profile.watched_episodes.all()
    
    context = {
        'watched_movies': watched_movies,
        'watched_episodes': watched_episodes,
    }
    return render(request, 'accounts/watch_history.html', context)
