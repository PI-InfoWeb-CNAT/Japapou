from django.contrib import admin  # type: ignore
from .models import *

admin.site.register(User)
