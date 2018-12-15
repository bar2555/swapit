from django.contrib import admin
from .models import Item

# Register your models here.

# register Item so that admin gives it an admin interface
admin.site.register(Item)
