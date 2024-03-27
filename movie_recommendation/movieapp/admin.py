from django.contrib import admin
from .models import Category,Movie,ReviewRating


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields ={'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ['Title','category','user']

    list_per_page = 20
admin.site.register(Movie,MovieAdmin)
admin.site.register(ReviewRating)