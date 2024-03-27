from django.shortcuts import render,redirect,reverse
from . models import WhishMovie
from movieapp.models import Movie
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def add_to_whishlist(request,movie_id):
    movie=Movie.objects.get(id=movie_id)
    print(movie.Title)
    try:
        whish_list_movie=WhishMovie.objects.get(user=request.user,movie=movie)
        if whish_list_movie:
            messages.info(request, 'Movie already added to whish list')
            return redirect('whishlist:movie_whish')
    except:
        whish_list_movie=WhishMovie.objects.create(user=request.user,movie=movie)
        whish_list_movie.save()
    return redirect('whishlist:movie_whish')


@login_required(login_url='signin')
def movie_whish(request):
    wish_movies=WhishMovie.objects.filter(user=request.user)
    context={
        'wish_movies':wish_movies
    }
    return render(request,'whish_list.html',context)

def delete_whish_movie(request,wishmovie_id):
    whish_movie=WhishMovie.objects.get(id=wishmovie_id)
    whish_movie.delete()
    return HttpResponseRedirect(reverse('whishlist:movie_whish'))