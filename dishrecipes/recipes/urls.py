from django.urls import path, re_path, register_converter
from recipes import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('find/', views.find, name='find'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('add/', views.add_recipe, name='add'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.show_post,
         name='post'),
    path('category/<int:cat_id>/', views.show_category,
         name='category'),
]
