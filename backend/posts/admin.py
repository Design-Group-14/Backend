from django.contrib import admin
from .models import Post

from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'latitude', 'longitude', 'location', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')


