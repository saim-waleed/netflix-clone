from django.contrib import admin
from .models import Category, Movie, TVShow, Episode, UserProfile, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'is_featured', 'is_trending')
    list_filter = ('categories', 'is_featured', 'is_trending')
    search_fields = ('title', 'description')
    date_hierarchy = 'release_date'

@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'is_featured', 'is_trending')
    list_filter = ('categories', 'is_featured', 'is_trending')
    search_fields = ('title', 'description')
    date_hierarchy = 'release_date'

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('tv_show', 'title', 'season_number', 'episode_number')
    list_filter = ('tv_show', 'season_number')
    search_fields = ('title', 'description', 'tv_show__title')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_watchlist_count', 'get_watched_count')
    search_fields = ('user__username',)

    def get_watchlist_count(self, obj):
        return obj.watchlist.count()
    get_watchlist_count.short_description = 'Watchlist'

    def get_watched_count(self, obj):
        return obj.watched_movies.count() + obj.watched_episodes.count()
    get_watched_count.short_description = 'Watched'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_content', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'movie__title', 'tv_show__title', 'comment')

    def get_content(self, obj):
        return obj.movie.title if obj.movie else obj.tv_show.title
    get_content.short_description = 'Content'
