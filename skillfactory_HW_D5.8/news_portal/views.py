from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from .models import Post, Category
from datetime import datetime

from .forms import NewsForm, ArticleForm
from .filters import PostFilter
from django.urls import reverse_lazy
from django.urls import reverse

from django.contrib.auth.mixins import PermissionRequiredMixin




class NewsListView(ListView):
    model = Post
    queryset = Post.objects.filter().order_by('-dateCreation')
    template_name = 'news_list.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'post'



class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'



class NewsSearchView(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        filter_form = PostFilter(self.request.GET, queryset=super().get_queryset())
        news = filter_form.qs

        selected_date = self.request.GET.get('date')
        selected_time = self.request.GET.get('time')

        if selected_date and selected_time:
            datetime_str = f'{selected_date} {selected_time}'
            selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            news = news.filter(dateCreation__gte=selected_datetime)

        selected_category = self.request.GET.get('postCategory')

        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = PostFilter(self.request.GET, queryset=self.get_queryset())
        categories = Category.objects.all()
        selected_category = self.request.GET.get('postCategory')
        context['filter_form'] = filter_form
        context['categories'] = categories
        context['selected_category'] = selected_category
        return context



class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post',)
    model = Post
    form_class = NewsForm
    success_url = reverse_lazy('news_list')
    template_name = 'news_create.html'
    #raise_exception = True

    def form_valid(self, form):
        form.instance.categoryType = Post.NEWS  # Установка значения поля "categoryType" на "новость"
        return super().form_valid(form)

# Представление для редактирования новости
class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_post',)
    model = Post
    form_class = NewsForm
    template_name = 'news_edit.html'


    def get_success_url(self):
        return reverse('news_detail', args=[self.object.pk])

# Представление для удаления новости
class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = '/news/'  # URL для перенаправления после успешного удаления


# Представление для создания статьи
class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post',)
    model = Post
    form_class = ArticleForm
    template_name = 'article_create.html'


    def form_valid(self, form):
        form.instance.categoryType = Post.ARTICLE  # Установка значения поля "categoryType" на "статья"
        return super().form_valid(form)

# Представление для редактирования статьи
class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.change_post',)
    model = Post
    form_class = ArticleForm
    template_name = 'article_edit.html'


    def get_success_url(self):
        return reverse('news_detail', args=[self.object.pk])

# Представление для удаления статьи
class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = '/articles/'
