from django.urls import path, re_path, register_converter
from recipes import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.RecipesHome.as_view(), name='home'),
    path('find/', views.find, name='find'),
    # path('find/<slug:slug>/', views.find.as_view(), name='find'),
    # path('archive/<year4:year>/', views.archive, name='archive'),
    # path('add/', views.addpage, name='add'),
    path('add/', views.AddPage.as_view(),
         name='add'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    # path('post/<slug:post_slug>/', views.show_post,
    #      name='post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', views.show_category,
    #      name='category'),
    path('category/<slug:cat_slug>/', views.RecipesCategory.as_view(),
         name='category'),
    # path('tag/<slug:tag_slug>/',
    #      views.show_tag_postlist, name='tag'),
    path('tag/<slug:tag_slug>/',  views.TagPostList.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),
]
