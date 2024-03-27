from django.urls import path,include
from . import views
app_name='whishlist'

urlpatterns = [
    path('movie/add_to_wishlist/<int:movie_id>/',views.add_to_whishlist,name='add_to_whishlist'),
    path('movie/whishlist/',views.movie_whish,name='movie_whish'),
    path('mvovie/delete_whish_movie/<int:wishmovie_id>/',views.delete_whish_movie,name='delete_whish_movie'),

]
