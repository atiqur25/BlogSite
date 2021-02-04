from django.db import models

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import  RichTextUploadingField
from django.http import HttpResponse






# Create your models here.


class Author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    profile_picture = models.FileField(blank=True)
    details = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return self.name.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    article_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body =RichTextUploadingField()
    image = models.FileField()
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="%s" width="100px" height="100px" />' % (self.image.url))

    image_tag.short_description = 'Image'

    def image_url(self):
        return self.image.url

    def __str__(self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Article, on_delete=models.CASCADE)
    email=models.EmailField()
    comment=models.TextField()

    def __str__(self):
        return self.post.title



