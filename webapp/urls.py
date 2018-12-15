from django.urls import include, path
from django.contrib import admin

from . import views

# define URL patterns
urlpatterns = [
    # map the index view to the default URL
    path('', views.index, name='index'),
    path('item/<int:item_id>', views.detail, name='detail'),
]
