from django.contrib import admin

from apps.comments.models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    exclude = ('liked_by',)
    list_display = ['description', 'pub_date', 'post', 'user', 'id']