from django.db import models

# Create your models here.

class Movie(models.Model):
    title_kor = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    poster_url = models.URLField()
    genre = models.CharField(max_length=255)
    showtime = models.IntegerField() #수정 
    release_date = models.DateField(null=True, blank=True)  # 2023-08-18
    plot = models.TextField()
    director_name = models.CharField(max_length=255)
    director_image_url = models.URLField()
    
    # 평점
    audience_score = models.FloatField(null=True, blank=True)  # 지금 이건 DB에 넣기 가능
    critic_score = models.FloatField(null=True, blank=True)    # 나중에 추가?
    netizen_score = models.FloatField(null=True, blank=True)   # 유저 평점 평균으로?

    def __str__(self):
        return self.title_kor


class Actor(models.Model):
    movie = models.ForeignKey(Movie, related_name='actors', on_delete=models.CASCADE) #actors로 역참조
    name = models.CharField(max_length=255)
    character = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.character})"
