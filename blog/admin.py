from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'created_at')  # Show these fields in the list view
    list_filter = ('created_at', 'author')  # Add filters to the sidebar
    search_fields = ('title', 'content')  # Allow search by title or content

admin.site.register(Post, PostAdmin)
