from django import forms

from .models import Article, Author,Category

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, TextInput, NumberInput, EmailInput, PasswordInput, Select, FileInput,Textarea



class create_postForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category'

        ]
        # widgets = {
        #     'title': TextInput(attrs={'class': 'input','placeholder': 'title'}),
        #     'image': FileInput(attrs={'class': 'input','placeholder': 'image'}),
        #     'category': Select(attrs={'class': 'input','placeholder': 'category'}),
        #     'body': Textarea(attrs={'class': 'input','placeholder': 'body'}),
        # }

class profileupdateForm(forms.ModelForm):
    class Meta:
        model=Author
        fields = ('profile_picture','details')
        widgets = {
            'profile_picture': FileInput(attrs={'class': 'input','placeholder': 'profile_picture',}),
            'details': Textarea(attrs={'class': 'input','placeholder': 'details'}),

        }

class createCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['name']
