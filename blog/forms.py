from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'summary': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 10}),
        }