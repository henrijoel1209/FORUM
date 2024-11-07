from django import forms
from .models import Post, Step, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['description', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
