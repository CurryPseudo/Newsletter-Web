from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import News, Tag, Comment, ReadRecord
# Create your views here.

class NewsList(ListView):
    template_name = "news/index.html"
    context_object_name = "manyNews"
    queryset = News.objects.filter(review_pass=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['all_tag'] = True
        context['favorite_tag'] = False
        context['cur_tag'] = None
        context['login_in'] = self.request.user.is_authenticated
        return context

    
class NewsTagDetail(DetailView):
    model = Tag
    template_name = "news/index.html"
    context_object_name = "cur_tag"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['all_tag'] = False
        context['favorite_tag'] = False
        context['manyNews'] = super().get_object().news.filter(review_pass=True)
        context['login_in'] = self.request.user.is_authenticated
        return context

from django.contrib.auth.models import User
from django.contrib import auth
from django import http
from django.urls import reverse
def login(request):
    from .forms import LoginForm
    if(request.user.is_authenticated):
        return http.HttpResponseRedirect(reverse("index"))

    if(request.method == "POST"):
        form = LoginForm(request.POST)
        if(form.is_valid()):
            user = auth.authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if(user == None):
                return render(request, 'news/login.html', {"error" : "用户认证失败"})
            else:
                auth.login(request, user)
                return http.HttpResponseRedirect(reverse("index"))
        return render(request, 'news/login.html', {"error" : "表单不合法", "form" : form})

    form = LoginForm()
    return render(request, 'news/login.html', {'form' : form})


def register(request):
    from .forms import RegisterForm
    if(request.method == "POST"):
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if(user == None):
                return render(request, 'news/register.html', {"error" : "注册失败，请检查注册信息"})
            auth.login(request, user)
            return http.HttpResponseRedirect(reverse("index"))
        return render(request, 'news/register.html', {"error" : "表单不合法"})
    else:
        if(request.user.is_authenticated):
            return http.HttpResponseRedirect(reverse("index"))
        return render(request, 'news/register.html')

from django.db.models import Count
from datetime import datetime
import random
class NewsDetail(DetailView):
    queryset = News.objects.filter(review_pass=True)
    template_name = "news/news_detail.html"
    context_object_name = "news"
    def get_context_data(self, **kwargs):
        news = self.get_object()
        if(self.request.user.is_authenticated):
            rr, _ = ReadRecord.objects.get_or_create(news=news, user=self.request.user)
            rr.time = datetime.now()
            rr.save()
        context = super().get_context_data(**kwargs)
        context['login_in'] = self.request.user.is_authenticated
        cur_news = self.get_object()
        relative_tags = cur_news.tags.all()
        relative_news = News.objects.none()
        for tag in relative_tags:
            relative_news = relative_news.union(tag.news.all())
        relative_news = sorted(relative_news, key=lambda x:random.random())
        context['relative_news_list'] = relative_news[:16]
        return context

def account(request):
    user = request.user
    if(user.is_authenticated):


        return render(request, "news/account.html", {'user' : user})
    else:
        return http.HttpResponseRedirect(reverse("index"))

def logout(request):
    auth.logout(request)
    return http.HttpResponseRedirect(reverse("login"))

def home(request):
    return http.HttpResponseRedirect(reverse("index"))

def favroite_news(request, pk):
    if(request.user.is_authenticated):
        news = News.objects.get(id=pk)
        if(news != None):
            if(len(news.favorited.all().filter(id=request.user.id)) != 0):      
                return http.HttpResponse("1")
    return http.HttpResponse("0")

def publish_news(request):
    if(not request.user.is_authenticated or request.method != "POST"):
        return http.HttpResponseForbidden()
    from json import loads
    data = loads(request.body)
    print(request.body)
    tags = Tag.objects.filter(name__in=data['label'])
    import datetime
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    newNews = News.objects.create(title=data['title'], pub_user=request.user, author=request.user.username, cover_image=data['PicUrl'], pub_date = date, content=data['article'], review_pass=False)
    newNews.tags.set(tags)
    newNews.save()
    return http.HttpResponse("1")
    
def favorite_news_post(request, pk, f):
    if(not request.user.is_authenticated):
        return http.HttpResponseForbidden()
    news = News.objects.get(id=pk)
    if(f == 1):
        news.favorited.add(request.user)
        return http.HttpResponse("Favorite success")
    else:
        news.favorited.remove(request.user)
        return http.HttpResponse("Unfavorite success")

def comment_post(request, pk, content):
    if(not request.user.is_authenticated):
        return http.HttpResponseForbidden()
    news = News.objects.get(id=pk)
    from datetime import datetime
    now = datetime.now()
    Comment.objects.create(user=request.user, content=content, pub_date=now, news=news)
    return http.HttpResponse("Comment sent ok")

def search(request, content):
    context = {}
    context['login_in'] = request.user.is_authenticated
    context['news_list'] = News.objects.filter(title__contains=content, review_pass=True)
    return render(request, "news/search.html", context)


