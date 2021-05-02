from rest_framework import serializers
from Posts.models import Post
from django import forms
 
class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
 
class PostValidator(forms.Form) :
    username = forms.CharField()
    tweet_text = forms.CharField()
 