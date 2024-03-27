from django.db import models
from django.urls import reverse
from  django.contrib.auth.models import User
from django.db.models import Avg,Count

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    image=models.ImageField(upload_to='category',blank=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse('movieapp:movie_by_category',args=[self.slug])

class Movie(models.Model):
    Title = models.CharField(max_length=255,unique=True)

    Poster=models.ImageField(upload_to='movie',blank=True)
    Description=models.TextField(blank=True)
    Release_date=models.DateField()
    Actors = models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    Trailer_link=models.TextField(blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering =('Title',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    def __str__(self):
        return '{}'.format(self.Title)

    def get_url(self):
        #return reverse('movieapp:movieDetail',args=[self.category.slug,self.slug])
        return reverse('movieapp:movieDetail', args=[self.id])
    def countReview(self):
        reviews=ReviewRating.objects.filter(movie=self,status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
        return count

    def averageReview(self):
        reviews = ReviewRating.objects.filter(movie=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
class ReviewRating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    review=models.TextField(max_length=255,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
