from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import News, Tag
# Create your views here.

class NewsList(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "manyNews"
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
        context['manyNews'] = super().get_object().news.all()
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

class NewsDetail(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = "news"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_in'] = self.request.user.is_authenticated
        cur_news = self.get_object()
        relative_tags = cur_news.tags.all()
        relative_news = News.objects.none()
        for tag in relative_tags:
            relative_news = relative_news.union(tag.news.all())
        context['relative_tags'] = relative_tags
        return context

def account(request):
    user = request.user
    if(user.is_authenticated):
        return render(request, "news/account.html", {'user' : user})
    else:
        return http.HttpResponseRedirect(reverse("index"))

def home(request):
    return http.HttpResponseRedirect(reverse("index"))