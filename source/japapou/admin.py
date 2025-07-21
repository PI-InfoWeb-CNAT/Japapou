from django.contrib import admin  # type: ignore
from japapou.models.menu import Menu
from japapou.models.prato import Prato
from japapou.models.cardapio import Cardapio
from japapou.models.user import User


admin.site.register(User)
admin.site.register(Menu)
admin.site.register(Prato)
admin.site.register(Cardapio)
