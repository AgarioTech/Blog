from apps.posts.models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'date'}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'wrapp_img', 'pub_date']

class CommentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "comment-input", "autofocus": "autofocus", "placeholder": "Написать комментарий"}), label='')
    class Meta:
        model = Comment
        fields = ["description"]
