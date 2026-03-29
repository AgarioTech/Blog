from rest_framework import serializers

from apps.posts.models import Post

from apps.categories.models import Category


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    is_authenticated = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    set_bookmark = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.username')
    image = serializers.SerializerMethodField()
    wrapp_img = serializers.SerializerMethodField()
    user_id = serializers.CharField(source='user.id')
    comment_count = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'pub_date', 'views_count',
                  'user', 'comment_count', 'liked_by', 'image', 'wrapp_img',
                  'id', 'user_id', 'bookmark_user', 'post_type', 'tag',
                  'likes', 'liked', 'is_authenticated', 'user_id', 'bookmark_count',
                  'set_bookmark']


    def get_bookmark_count(self, obj):
        return obj.bookmark_user.count()

    def get_set_bookmark(self, obj):
        request = self.context.get('request')
        return obj.bookmark_user.filter(id=request.user.id).exists()

    def get_likes(self, obj):
        return obj.liked_by.count()

    def get_liked(self, obj):
        request = self.context.get('request')
        return obj.liked_by.filter(id=request.user.id).exists()

    def get_is_authenticated(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated

    def get_user_id(self, obj):
        request = self.context.get('request')
        return request.user.id

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_category(self, obj):
        if obj.category:
            return obj.category.cat_title
        return 'Без темы'

    def get_tag(self, obj):
        if obj.category:
            return obj.category.tag
        return None

    def get_wrapp_img(self, obj):
        if obj.wrapp_img and hasattr(obj.wrapp_img, 'url'):
            return obj.wrapp_img.url
        return None

    def get_image(self, obj):
        if obj.user.image:
            return obj.user.image.url
        return None

class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='cat_title',
        allow_null=True,
        required=False,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ['title', 'wrapp_img', 'category',
                  'content', 'post_type']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

