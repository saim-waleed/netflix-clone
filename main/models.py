from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text='Duration in minutes')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video_file = models.FileField(upload_to='movies/')
    categories = models.ManyToManyField(Category, related_name='movies')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class TVShow(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    categories = models.ManyToManyField(Category, related_name='tv_shows')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Episode(models.Model):
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    duration = models.IntegerField(help_text='Duration in minutes')
    video_file = models.FileField(upload_to='episodes/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['season_number', 'episode_number']

    def __str__(self):
        return f"{self.tv_show.title} - S{self.season_number:02d}E{self.episode_number:02d} - {self.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    watchlist = models.ManyToManyField(Movie, blank=True, related_name='in_watchlist')
    watched_movies = models.ManyToManyField(Movie, blank=True, related_name='watched_by')
    watched_episodes = models.ManyToManyField(Episode, blank=True, related_name='watched_by')

    def __str__(self):
        return self.user.username

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='user_ratings')
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE, null=True, blank=True, related_name='user_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'movie'], ['user', 'tv_show']]

    def __str__(self):
        content = self.movie.title if self.movie else self.tv_show.title
        return f"{self.user.username}'s rating for {content}"
