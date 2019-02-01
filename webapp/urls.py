from django.urls import include, path
# from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views # use django's built in views for authorisation

from . import views

# define URL patterns
urlpatterns = [
    # map the index view to the default URL
    path('', views.index, name='index'),
    path('item/<int:item_id>', views.item_detail, name='item_detail'),
    path('newitem', views.item_add, name='item_add'),
    path('signup', views.signup, name='signup'),
    # logout and then redirect to index using next_page variable
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
