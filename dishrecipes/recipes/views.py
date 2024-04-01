from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import slugify

from recipes.models import Recipes, Category, TagPost

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


def index(request):
    posts = Recipes.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'recipes/index.html',
                  context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category,
                                 slug=cat_slug)
    posts = Recipes.published.filter(cat_id=category.pk)
    data = {
        'title': f'Категория {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'recipes/cats.html',
                  context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Recipes.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'recipes/index.html',
                  context=data)


def find(request):
    posts = Recipes.published.all()
    data = {'title': 'Поиск рецептов',
            'menu': menu,
            'posts': posts,
            }
    return render(request, 'recipes/cats.html',
                  context=data)


def archive(request, year):
    if year > 2024:
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Архив рецептов по годам</h1><p >{year}</p>")


def show_post(request, post_slug):
    post = get_object_or_404(Recipes, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'recipes/post.html',
                  context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def add_recipe(request):
    return render(request, 'recipes/add.html',
                  {'title': 'Добавить свой рецепт', 'menu': menu})


def about(request):
    return render(request, 'recipes/about.html',
                  {'title': 'О сайте', 'menu': menu})


def login(request):
    return render(request, 'recipes/login.html',
                  {'title': 'Вход', 'menu': menu})
