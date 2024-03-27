from django.db import models
from django.contrib.auth.models import User
from movieapp.models import Movie

# Create your models here.
class WhishMovie(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.movie}'
