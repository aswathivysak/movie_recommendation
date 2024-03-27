from django.shortcuts import render,get_object_or_404
from  django.shortcuts import render,redirect
from .models import Movie,Category,ReviewRating
from .forms import  MovieForm,RatingForm
from django.contrib import messages
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

from django.contrib.auth.decorators import login_required
from  django.db.models import Q

# Create your views here.
def index(request,cat_slug=None):
    c_page=None
    movie=None
    if cat_slug!=None:
        c_page=get_object_or_404(Category,slug=cat_slug)

        movies=Movie.objects.all().filter(category=c_page)
        paginator = Paginator(movies, 8)
        page = request.GET.get('page')
        paged_movies = paginator.get_page(page)
    else:
        movies = Movie.objects.all()
        paginator=Paginator(movies,8)
        page=request.GET.get('page')
        paged_movies=paginator.get_page(page)

    return render(request,'index.html',{'category':c_page,'movies':paged_movies})

#def movieDetail(request,cat_slug,movie_slug):
@login_required(login_url='signin')
def movieDetail(request,movie_id):
    try:
        #movie=Movie.objects.get(category__slug=cat_slug,slug=movie_slug)
        movie = Movie.objects.get(id=movie_id)
        print(request.user)
        print(movie.user)
    except Exception as e:
         raise e
    #get the review
    reviews=ReviewRating.objects.filter(movie_id=movie_id,status=True)

    return render(request,'movie_detail.html',{'movie':movie,'reviews':reviews})

@login_required(login_url='signin')
def movieAdd(request):
    category=Category.objects.all()
    user = request.user
    print(user)
    if request.method == 'POST':

        title=request.POST.get('title',)
        print(title)
        description = request.POST.get('description',)
        print(description)
        link = request.POST.get('link',)
        print(link)
        actors = request.POST.get('actors', )
        print(actors)
        Date = request.POST.get('date',)
        print(Date)
        category = request.POST.get('category',)
        print(category)
        cat_obj=Category.objects.get(id=category)
        print(cat_obj)
        poster = request.FILES['img']
        print(poster)
        movie = Movie(Title=title, Description=description,Trailer_link=link,Release_date= Date,Actors=actors,category=cat_obj,Poster=poster,user=user)
        movie.save()
        return redirect('/')


    context={
        'category':category,
    }
    return render(request,'movie_add.html',context)

def update(request,id):
    movie = Movie.objects.get(id=id)
    print(movie)
    if request.method == 'POST':
        form=MovieForm(request.POST,request.FILES,instance=movie)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=MovieForm(instance=movie)
        print(form)
    return render(request,'update.html',{'movie':movie,'form':form})
def delete(request,id):
    if request.method == 'POST':
        movie=Movie.objects.get(id=id)
        movie.delete()
        return redirect('/')

    return render(request,'delete.html')

#revie submiting
def submit_review(request,movie_id):
    url=request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            # revie already exists
            reviews=ReviewRating.objects.get(user__id=request.user.id,movie__id=movie_id)
            form=RatingForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! your reviewhasbeen updated')
            return redirect(url)
            # we need to return same page
        except ReviewRating.DoesNotExist:
            form=RatingForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.review=form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.rating = form.cleaned_data['rating']
                data.rating = form.cleaned_data['rating']
                data.movie_id=movie_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thank you! your reviewhasbeen submited')
                return redirect(url)
def searchMovie(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            movies=Movie.objects.all().filter(Q(Title__contains=keyword) | Q(Description__contains=keyword))
            movie_count=movies.count()
            context={
                'movies':movies,
                'keyword':keyword,
                'movie_count':movie_count,
            }
    return render(request,'search.html',context)