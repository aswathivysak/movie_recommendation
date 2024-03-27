from django.urls import path,include
from . import views
app_name='movieapp'

urlpatterns = [
        path("",views.index,name='index'),
        path('<slug:cat_slug>/',views.index,name='movie_by_category'),
        #path('<slug:cat_slug>/<slug:movie_slug>/moviedetail/',views.movieDetail,name='movieDetail'),
        path('movie/<int:movie_id>/', views.movieDetail, name='movieDetail'),
        path('movieAdd/add/',views.movieAdd,name='movieAdd'),
        path('update/<int:id>/', views.update, name='update'),
        path('delete/<int:id>/', views.delete, name='delete'),
        path('submit_review/<int:movie_id>/',views.submit_review,name='submit_review'),
        path('searchMovie/movie/',views.searchMovie,name='searchMovie')

]
