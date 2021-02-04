from django.urls import path
from .views import Pdf_views

from . import views

urlpatterns = [
    path('',views.Homepage,name='home'),
    path('single/<int:id>/',views.singlepage,name='single_page'),
    path('category/<name>/',views.categoryTopic,name='category_page'),
    path('author/<name>',views.author,name='author'),
    path('login/',views.getlogin,name="login"),
    path('logout/',views.getlogout,name="logout"),
    path('register/',views.Registertion,name="register"),
    path('search/',views.search,name="search"),
    path('create_post/',views.create_post,name="create_post"),
    path('profile/',views.userprofile,name="userprofile"),
    path('update/<int:pid>/',views.postUpdate,name="update"),
    path('delete/<int:pid>/',views.postDelete,name="delete"),
    path('userProfileUpdate/',views.userProfileUpdate,name="userProfileUpdate"),
    path('allCategoryShow/',views.AllCategoryShow,name="allCategoryShow"),
    path('createCategory/',views.createCategory,name="createCategory"),
    path('deletedCategory/<int:id>/',views.DeletedCategory,name="DeletedCategory"),
    path('UpdateCategory/<int:id>/',views.UpdateCategory,name="UpdateCategory"),
    path('DeleteComment/<int:id>/<int:pid>/',views.DeleteComment,name="DeleteComment"),
    # path('EditComment/<int:id>/<int:pid>/',views.EditComment,name="EditComment"),
    # htmt to pdf
    path('pdf/<int:id>/',views.Pdf_views.as_view(),name='savepdf'),
    # pdf file
    path('download_pdf/',views.download_pdf,name='download_pdf'),

    # registration  confrimation
    # path('activate/<uid>/<token>/',views.activate,name="activate"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]

