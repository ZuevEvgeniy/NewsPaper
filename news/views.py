# Create your views here.
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from datetime import datetime
from .models import Post, Category
from .filters import NewsFilter
from .forms import PostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class NewsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


@method_decorator(login_required, name='dispatch')
class PostCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == "/news/article/create/":
            post.type="01"
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@method_decorator(login_required, name='dispatch')
class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@method_decorator(login_required, name='dispatch')
class PostDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['new_post'] = "Свежие новости сегодня!"
        context['filterset'] = self.filterset
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = "Вы в рассылке категории"
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class CategoryListView (NewsList):
    model= Post
    template_name = "categories.html"
    context_object_name = "category_news_list"

    def get_queryset(self):
        self.category = get_object_or_404(Category,id= self.kwargs ['pk'])
        queryset=Post.objects.filter(category=self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_subscriber"] = self.request.user not in self.category.subscribers.all()
        context['category']=self.category
        return context

