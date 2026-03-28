from apps.posts.models import Post
from apps.comments.models import Comment
from django import forms


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'date'}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'wrapp_img', 'pub_date']

