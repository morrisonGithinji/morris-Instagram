from django import forms
from .models import Post, Comment,Profile

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    exclude = ['profile','likes', 'comment','user']
  
class CommentForm(forms.ModelForm):
  class Meta:
   model = Comment
   exclude = ['post','user']
   
class ProfileForm(forms.ModelForm):
  bio= forms.CharField(widget=forms.TextInput(), max_length=260, required=False)
  profile_photo= forms.ImageField(required=False)
  
  class Meta:
    model = Profile
    exclude = ['user']