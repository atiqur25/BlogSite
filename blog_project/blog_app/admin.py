from django.contrib import admin
from blog_app.models import Author,Category,Article,Comment

# Register your models here.
class authorAdmin(admin.ModelAdmin):
    list_display = ['__str__','name','create_at']
    search_fields = ["__str__","details"]
    list_filter = ['create_at']
    list_per_page = 10

    class Meta:
        Model = Author


admin.site.register(Author,authorAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    class Meta:
        Model = Category

admin.site.register(Category,CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['article_author','title','create_at','image_tag']
    list_filter = ['title','article_author']

    class Meta:
        Model = Article

admin.site.register(Article,ArticleAdmin)


# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['post','name','create_at','email']
#     list_filter = ['name','post']
#
#     class Meta:
#         Model = Comment

admin.site.register(Comment)