from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import slugify

from recipes.models import Recipes

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
    }
    return render(request, 'recipes/index.html',
                  context=data)


def show_category(request, cat_id):
    data = {
        'title': 'Поиск рецептов',
        'menu': menu,
        'posts': Recipes.published.all(),
        'cat_selected': cat_id,
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


def find(request):
    posts = Recipes.published.all()
    data = {'title': 'Поиск рецептов',
            'menu': menu,
            'posts': posts,
            }
    return render(request, 'recipes/find.html',
                  context=data)


def login(request):
    return render(request, 'recipes/login.html',
                  {'title': 'Вход', 'menu': menu})
