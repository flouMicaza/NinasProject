from django.contrib import admin

# Register your models here.
from usuarios.models import User

admin.site.register(User)