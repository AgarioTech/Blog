from django.contrib import admin

from apps.posts.models import Post, Comment, Category, SiteError


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	exclude = ('liked_by',)
	list_display = ['title', 'category', 'pub_date', 'status', 'id', 'post_type']
	list_filter = ['category', 'pub_date', 'status', 'bookmark_user', 'post_type']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	exclude = ('liked_by',)
	list_display = ['description', 'pub_date', 'post', 'user', 'id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['cat_title', 'image']

@admin.register(SiteError)
class SiteErrorAdmin(admin.ModelAdmin):
	list_display = ['title', 'description', 'status']




