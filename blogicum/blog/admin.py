from django.contrib import admin

from .models import Category, Comment, Location, Post



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


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'created_at',
        'author'
    )
    search_fields = (
        'text',
    )
    list_filter = (
        'created_at',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
