from django import forms

from .models import Article, Author, Category

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, TextInput, NumberInput, EmailInput, PasswordInput, Select, FileInput, Textarea


class create_postForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category'

        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your title  '}),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'chose your Image'}),
            'category': Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            # 'body': Textarea(attrs={'cols': 10, 'rows': 80}),
        }


class profileupdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('profile_picture', 'details')
        widgets = {
            'profile_picture': FileInput(attrs={'class': 'form-control', 'placeholder': 'profile_picture', }),
            'details': Textarea(attrs={'class': 'form-control', 'rows': 5}),

        }


class createCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'add category   '}),
        }
