from django import forms

from apps.comments.models import Comment


class CommentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "comment-input", "autofocus": "autofocus", "placeholder": "Написать комментарий"}), label='')
    class Meta:
        model = Comment
        fields = ["description"]