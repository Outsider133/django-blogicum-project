from .models import Category, Location, Post

from django.contrib import admin


admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug'
    )
    search_fields = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
        'is_published'
    )
    search_fields = (
        'title',
        'text'
    )
    list_filter = (
        'pub_date',
        'is_published'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
