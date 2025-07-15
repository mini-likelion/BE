from django.db import models
from django.conf import settings
from movies.models import Movie


# Create your models here.

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model): #N대 N 관계 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings') #N
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField() #평점 