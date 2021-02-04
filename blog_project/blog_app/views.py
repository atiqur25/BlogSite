from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect,get_object_or_404,Http404

from blog_app.models import Author,Category,Article,Comment

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from django.core.paginator import Paginator
# search er jonno
from django.db.models import Q
# messages er
from django.contrib import messages

from .forms import create_postForm,profileupdateForm,createCategoryForm

# varification er jonno
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes



#pdf er code
from django.views.generic import View
from .render import render_to_pdf
from django.http import HttpResponse

#download pdf
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound


def Homepage(request):
    post=Article.objects.all().order_by('-id')
    # paginator start
    page = request.GET.get('page',1)

    paginator = Paginator(post,6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    #
    # paginator = Paginator(post,per_page=1)  # Show 10 contacts per page.
    # page_number = request.GET.get('page', 1)
    # total_article = paginator.get_page(page_number)
    # paginator end
    data={
        "article_post":users,
        # 'paginator': paginator,
        # 'page_number': int(page_number)
    }
    return render(request,"index.html",data)

def search(request):
    try:
        q = request.POST.get('q')

    except:
        q = None
    if q:
        search_pro =Article.objects.filter(title__icontains=q)

        data = {
            "article_post": search_pro,

        }
        return render(request,'search.html',data)

    else:
        data = {
        }
        return render(request,'Eorr_440.html',data)


def author(request,name):
    post_author = get_object_or_404(User,username=name) # name = je auth name click korbo
    auth = get_object_or_404(Author,name=post_author.id) # clik name Author model import
    # post = Article.objects.filter(article_author=post_author.id) # author all post je kono ekta korle hobe
    post = Article.objects.filter(article_author=auth.id) # author all post
    # return HttpResponse(post)

    # paginator start
    paginator = Paginator(post,4)  # Show 10 contacts per page.
    page_number = request.GET.get('page')
    total_article = paginator.get_page(page_number)
    # paginator End

    data = {
        "auth": auth,
        "post": total_article,
    }
    return render(request,"author_all_post.html",data)

def singlepage(request,id):

    single_post=get_object_or_404(Article,id=id)
    first = Article.objects.first()
    last = Article.objects.last()
    # comment er jonno
    if request.user.is_authenticated:
        current_email = request.user.email
        if request.method == 'POST':
            comment = request.POST['comment']
            data = Comment(comment=comment)
            data.email = current_email
            data.post = single_post
            # return HttpResponse(data)
            data.save()
    # comment
    commentShow=Comment.objects.filter(post_id=id)
    total_comment=0
    for p in commentShow:
        i=1
        total_comment = total_comment+i
        i=i+1

    ralated_post=Article.objects.filter(category=single_post.category).exclude(id=id)[:4]

    data={
        "single_post":single_post,
        "first":first,
        "last":last,
        "ralated_post":ralated_post,
        "commentShow":commentShow,
        "total_comment":total_comment,
    }
    return render(request,"single_page.html",data)

def categoryTopic(request,name): # category show
    cat=get_object_or_404(Category,name=name) # name import Category model
    post=Article.objects.filter(category=cat.id) #category import Article
    # paginator start
    paginator = Paginator(post,per_page=4)  # Show 10 contacts per page.
    page_number = request.GET.get('page',1)
    total_article = paginator.get_page(page_number)
    # paginator End

    data={
        "post":total_article.object_list,
        "cat":cat,
        'paginator': paginator,
        'page_number': int(page_number)
    }
    return render(request,'category.html',data)


def Registertion(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['fist_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password1=request.POST['Password1']
        password2=request.POST['Password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'teken username')
                return redirect('register')

            elif User.objects.filter(email=email).exists():

                messages.info(request,'teken email')
                return redirect('register')
            else:
                x = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,
                                             password=password1,)
                                # # User Registration With Email Verification in Django
                x.is_active = False # varefication er jonno
                x.save()
                # #auto profile create er jonno
                user = User.objects.latest('id')
                data = Author()
                data.name_id =user.id
                data.profile_picture = "profile/avatar.jpg"
                data.save()
                # # profile picture End

                current_site = get_current_site(request)
                mail_subject = "Activate Your blog site Account"
                message = render_to_string('confrim_email.html',{
                    'user': x,
                    'domain': current_site.domain,
                    # 'uid': x.id,
                    'uid': urlsafe_base64_encode(force_bytes(x.pk)),
                    'token': default_token_generator.make_token(x), # token.py inport account_activation_token
                })
                to_email =request.POST['email']
                to_list=[to_email]
                from_email=settings.EMAIL_HOST_USER
                send_mail(mail_subject,message,from_email,to_list,fail_silently=True)
                return render(request, 'thanks_for.html')
                # return HttpResponse("thanks for registertion send code your email ")


        else:
            messages.info(request,'password not matching ')
            return redirect('register')
        return redirect('home')

    else:
        return render(request,'register.html')


def getlogin(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)

            if auth is not None:
                login(request, auth)

                # data = Author()
                # # # auto profile avatar picture save hobe tar code
                # current_user = request.user
                # data.profile_picture = "profile/avatar.jpg"
                # data.save()
                # # # profile picture End
                return redirect('home')
            else:
                messages.add_message(request, messages.WARNING, 'username or password mismatch')
                return render(request, "login.html")

    return render(request, "login.html")


def getlogout(request):
    logout(request)
    return redirect('home')

def create_post(request):
    if request.user.is_authenticated:
        user_Name = get_object_or_404(Author,name=request.user.id)
        form = create_postForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = user_Name
            instance.save()
            return redirect('home')
        data = {
            "form": form,
        }
        return render(request,'create_post.html',data)
    else:
        return redirect('login')

def postUpdate(request,pid):
    if request.user.is_authenticated:
        user_Name = get_object_or_404(Author,name=request.user.id)
        post=get_object_or_404(Article,id=pid)
        form = create_postForm(request.POST or None,request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = user_Name
            instance.save();
            return redirect('home')
        data = {
            "form": form,
        }
        return render(request,'create_post.html',data)
    else:
        return redirect('login')

def postDelete(request,pid):
    if request.user.is_authenticated:
        post=get_object_or_404(Article,id=pid)
        post.delete()
        messages.add_message(request,messages.WARNING,'  your post successfully deleted')
        return redirect('userprofile')

    else:
        return redirect('login')

def userprofile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(Author, name=request.user.id)
        user_all_post=Article.objects.filter(article_author=request.user.id)
        data={
            "post":user_all_post,
            "user":user,
        }

    return render(request,'user_profile.html',data)


def userProfileUpdate(request):
    if request.user.is_authenticated:
        current_user=request.user
        post=Author.objects.get(name_id=current_user.id)
        profile_form=profileupdateForm(request.POST or None,request.FILES or None,instance=post)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('userprofile')

    profile_form = profileupdateForm(instance=request.user)
    data={
        "profileForm":profile_form
    }
    return render(request, 'prifileudate.html',data)


def AllCategoryShow(request):
    all_category=Category.objects.all()
    data={
        "all_category":all_category,
    }
    return render(request, 'allcategoryShow.html',data)




def createCategory(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = createCategoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('allCategoryShow')

            data = {
                "form": form
            }
            return render(request,'createCategory.html',data)
        else:
            raise Http404('you are not authorized to access  this page ')
    else:
        return redirect('login')

def DeletedCategory(request,id):
    cat=get_object_or_404(Category, id=id)
    cat.delete()
    return redirect('allCategoryShow')

def UpdateCategory(request,id):
    cat=get_object_or_404(Category,id=id)
    form=createCategoryForm(request.POST or None,instance=cat)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('allCategoryShow')
    data={
        "form":form
    }

    return render(request,'updateCategory.html',data)

def DeleteComment(request,pid,id):
    comm=Comment.objects.filter(post_id=pid,id=id)
    comm.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # same page redirect


# registertin comfrimatin

# def activate(request,uid,token):
#     try:
#         user = User.objects.get(pk=uid)
#     except:
#         raise Http404("No user found ")
#     if user is not None and default_token_generator.check_token(user,token):
#         user.is_active = True
#         user.save()
#         # return HttpResponse("<h1> login now  </h1>")
#         return redirect('home')
#     else:
#         return HttpResponse('Activation link is invalid!')

#email varification   active link
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        raise Http404("No user found ")
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


# pdf create html2pdf
class Pdf_views(View):
    def get(self,request,id):
        # model theke data niye asbe query korte hobe
        try:
            query_data = get_object_or_404(Article, id=id)
        #
        except:
            Http404('Content not found')

        data = {
            "query_data": query_data,
        }
        # getting the template
        article_pdf = render_to_pdf('pdf1.html',data)
        return HttpResponse(article_pdf,content_type='application/pdf')




# Download pdf our
def download_pdf(request):
    fs = FileSystemStorage()
    filename = 'pdf_folder/atikur.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="atikur.pdf"' #user will be prompted with the browser’s open/save file
            response['Content-Disposition'] = 'inline; filename="atikur.pdf"' #user will be prompted display the PDF in the browser
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')
#
#


# def EditComment(request,pid,id):
#     com=get_object_or_404(Comment,id=id)
#     comm=Comment.objects.filter(post_id=pid,instance=com)
#     comm.save()
#     return render(request,"single_page.html",data)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # same page redirect