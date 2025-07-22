from django.contrib import admin  # type: ignore
from japapou.models import Menu, Period, Plate, User


admin.site.register(Menu)
admin.site.register(Period)
admin.site.register(Plate)
admin.site.register(User)
