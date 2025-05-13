from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Movie, TVShow, Episode, Category, UserProfile, Rating

def home(request):
    featured_movies = Movie.objects.filter(is_featured=True)[:5]
    trending_movies = Movie.objects.filter(is_trending=True)[:10]
    latest_movies = Movie.objects.order_by('-release_date')[:10]
    categories = Category.objects.all()

    context = {
        'featured_movies': featured_movies,
        'trending_movies': trending_movies,
        'latest_movies': latest_movies,
        'categories': categories,
    }
    return render(request, 'main/home.html', context)

def browse(request):
    category = request.GET.get('category')
    sort = request.GET.get('sort', '-release_date')
    
    movies = Movie.objects.all()
    if category:
        movies = movies.filter(categories__name=category)
    
    movies = movies.order_by(sort)
    
    paginator = Paginator(movies, 20)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    
    categories = Category.objects.all()
    
    context = {
        'movies': movies,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
    }
    return render(request, 'main/browse.html', context)

def search(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        tv_shows = TVShow.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        movies = Movie.objects.none()
        tv_shows = TVShow.objects.none()

    context = {
        'query': query,
        'movies': movies,
        'tv_shows': tv_shows,
    }
    return render(request, 'main/search.html', context)

@login_required
def watch_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Mark movie as watched
    profile = request.user.userprofile
    profile.watched_movies.add(movie)
    
    # Get user rating if exists
    user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
    
    context = {
        'movie': movie,
        'user_rating': user_rating,
    }
    return render(request, 'main/watch_movie.html', context)

@login_required
def watch_episode(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)
    
    # Mark episode as watched
    profile = request.user.userprofile
    profile.watched_episodes.add(episode)
    
    # Get next episode
    next_episode = Episode.objects.filter(
        tv_show=episode.tv_show,
        season_number=episode.season_number,
        episode_number=episode.episode_number + 1
    ).first()
    
    if not next_episode:
        next_episode = Episode.objects.filter(
            tv_show=episode.tv_show,
            season_number=episode.season_number + 1,
            episode_number=1
        ).first()
    
    context = {
        'episode': episode,
        'next_episode': next_episode,
    }
    return render(request, 'main/watch_episode.html', context)

@login_required
def toggle_watchlist(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        profile = request.user.userprofile
        
        if movie in profile.watchlist.all():
            profile.watchlist.remove(movie)
            added = False
        else:
            profile.watchlist.add(movie)
            added = True
        
        return JsonResponse({'added': added})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def rate_content(request, content_type, content_id):
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        if content_type == 'movie':
            content = get_object_or_404(Movie, id=content_id)
            rating, created = Rating.objects.get_or_create(
                user=request.user,
                movie=content,
                defaults={'rating': rating_value, 'comment': comment}
            )
        else:
            content = get_object_or_404(TVShow, id=content_id)
            rating, created = Rating.objects.get_or_create(
                user=request.user,
                tv_show=content,
                defaults={'rating': rating_value, 'comment': comment}
            )
        
        if not created:
            rating.rating = rating_value
            rating.comment = comment
            rating.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def api_movies(request):
    page = int(request.GET.get('page', 1))
    movies_per_page = 20
    
    movies = Movie.objects.all().order_by('-release_date')
    paginator = Paginator(movies, movies_per_page)
    
    try:
        movies_page = paginator.page(page)
    except:
        return JsonResponse({'movies': []})
    
    movies_data = [{
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'thumbnail': movie.thumbnail.url,
        'rating': float(movie.rating),
    } for movie in movies_page]
    
    return JsonResponse({'movies': movies_data})
