from django.contrib import admin

from apps.posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	exclude = ('liked_by',)
	list_display = ['title', 'category', 'pub_date', 'status', 'id', 'post_type']
	list_filter = ['category', 'pub_date', 'status', 'bookmark_user', 'post_type']

#
# @admin.register(SiteError)
# class SiteErrorAdmin(admin.ModelAdmin):
# 	list_display = ['title', 'description', 'status']




