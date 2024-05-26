from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import slugify
import uuid
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

import recipes
from recipes.forms import AddPostForm, UploadFileForm
from recipes.models import Recipes, Category, TagPost, UploadFiles
from recipes.utils import DataMixin

menu = [{'title': "Поиск рецептов", 'url_name': 'find'},
        {'title': "Войти", 'url_name': 'login'},
        {'title': "Добавить свой рецепт", 'url_name': 'add'},
        {'title': "О сайте", 'url_name': 'about'},
        ]

cats_db = [
    {'id': 1, 'name': 'Горячее'},
    {'id': 2, 'name': 'Закуски'},
    {'id': 3, 'name': 'Десерты'},
]


class RecipesHome(DataMixin, ListView):
    model = Recipes
    template_name = 'recipes/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница', cat_selected=0, )


class RecipesCategory(DataMixin, ListView):
    template_name = 'recipes/cats.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория ' + cat.name, cat_selected=cat.id, )

    def get_queryset(self):
        return Recipes.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


class TagPostList(DataMixin, ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Recipes.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Recipes
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    template_name = 'recipes/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['post'])

    def get_object(self, queryset=None):
        return get_object_or_404(Recipes.published,
                                 slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    model = Recipes
    fields = ['title', 'slug', 'content', 'is_published',
              'cat', 'tags', 'photo']

    # form_class = AddPostForm
    template_name = 'recipes/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Recipes
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'recipes/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


class DeletePage(DeleteView):
    model = Recipes
    success_url = reverse_lazy('home')
    template_name = 'recipes/delete.html'
    extra_context = {
        'menu': menu,
        'title': 'Удаление статьи',
    }


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def about(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             fp = UploadFiles(file=form.cleaned_data['file'])
#             fp.save()
#     else:
#         form = UploadFileForm()
#     return render(request, 'recipes/about.html',
#                   {'title': 'О сайте', 'menu': menu, 'form': form})
def about(request):
    contact_list = Recipes.published.all()
    paginator = Paginator(contact_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/about.html', {'page_obj':
                                                      page_obj, 'title': 'О сайте'})


def login(request):
    return render(request, 'recipes/login.html',
                  {'title': 'Вход', 'menu': menu})


def find(request):
    posts = Recipes.published.all()
    data = {'title': 'Поиск рецептов',
            'menu': menu,
            'posts': posts,
            }
    return render(request, 'recipes/cats.html', context=data)
