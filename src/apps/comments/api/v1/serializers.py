from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='user.image.url')
    username = serializers.CharField(source='user.username')
    likes = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    is_authenticated = serializers.SerializerMethodField()
    post = serializers.CharField(source='post.title')
    post_id = serializers.CharField(source='post.id')
    bookmarked_by = serializers.SerializerMethodField()
    set_bookmark = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['description', 'image', 'username', 'pub_date', 'likes',
                  'liked_by', 'id', 'liked', 'is_authenticated', 'post', 'post_id',
                  'bookmarked_by', 'set_bookmark']

    def get_set_bookmark(self, obj):
        request = self.context.get('request')
        return obj.bookmarked_by.filter(id=request.user.id).exists()

    def get_bookmarked_by(self, obj):
        return list(obj.bookmarked_by.values('id', 'username'))

    def get_likes(self, obj):
        return obj.liked_by.count()

    def get_liked_by(self, obj):
        return list(obj.liked_by.values('id', 'username'))

    def get_liked(self, obj):
        request = self.context.get('request')
        return obj.liked_by.filter(id=request.user.id).exists()

    def get_is_authenticated(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated
