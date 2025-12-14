from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Добавить эту строку

urlpatterns = [
    path('', RedirectView.as_view(url='bboard/')),  # Главная страница
    path('bboard/', include('bboard.urls')),
    path('admin/', admin.site.urls),
]