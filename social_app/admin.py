from django.contrib import admin
from .models import Profile, Post, Comment, PostLikes

# ==========================
# PROFILE
# ==========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('following',)  # dla łatwego wyboru obserwowanych profili

# ==========================
# POSTY
# ==========================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username')

# ==========================
# KOMENTARZE
# ==========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__content')

# ==========================
# POLUBIENIA (PostLikes)
# ==========================
@admin.register(PostLikes)
class PostLikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content')
