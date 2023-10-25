from django import forms
from blogs.models import Comment
from blogs.models import  Post


class PostCommentForm(forms.ModelForm):
    content = forms.CharField(label='Ingrese un comentario')
    class Meta:
        model = Comment
        fields = ['content']
        
        
class ReviewForm(forms.ModelForm):
    content = forms.CharField(label='Ingrese una review')
    class Meta:
        model = Post
        fields = ('title','content','album', 'rating')