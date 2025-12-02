from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ 
            'title',
            'text',
            'category',
            'location',
            'is_published',
            'pub_date',
            'image',
        ]
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M:%S',
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }
        labels = {
            'text': 'Текст комментария',
        }
