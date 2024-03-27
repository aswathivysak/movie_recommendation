from django import forms
from .models import Movie,ReviewRating
class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['Title','Description','Actors','category','Trailer_link','Release_date','Poster']

class RatingForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['review','rating']
