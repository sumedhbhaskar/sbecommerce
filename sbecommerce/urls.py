
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls.py"), namespace = 'core'),
    path('accounts/', include(allauth.urls)),

]
