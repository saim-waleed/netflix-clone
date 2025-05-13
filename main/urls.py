from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browse/', views.browse, name='browse'),
    path('search/', views.search, name='search'),
    path('watch/movie/<int:movie_id>/', views.watch_movie, name='watch_movie'),
    path('watch/episode/<int:episode_id>/', views.watch_episode, name='watch_episode'),
    path('watchlist/toggle/<int:movie_id>/', views.toggle_watchlist, name='toggle_watchlist'),
    path('rate/<str:content_type>/<int:content_id>/', views.rate_content, name='rate_content'),
    path('api/movies/', views.api_movies, name='api_movies'),
] 