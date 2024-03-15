from django.contrib import admin
from recipes import views
from django.urls import path, include
from recipes.views import page_not_found

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
]
