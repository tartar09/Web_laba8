from django.conf.urls.static import static
from django.contrib import admin
from dishrecipes import settings
from recipes import views
from django.urls import path, include
from recipes.views import page_not_found

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('users/', include('users.urls',
                           namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
