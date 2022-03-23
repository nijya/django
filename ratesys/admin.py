from django.contrib import admin

# Register your models here.
from .models import Module, Professor, Rate, User

admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(Rate)
admin.site.register(User)