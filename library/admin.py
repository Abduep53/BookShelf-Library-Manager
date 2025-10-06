from django.contrib import admin
from .models import Book, Profile


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'user', 'date_added')
    list_filter = ('status', 'date_added')
    search_fields = ('title', 'author')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')
    search_fields = ('user__username',)

