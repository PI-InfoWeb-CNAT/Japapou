from django.contrib import admin  # type: ignore
from japapou.models import *
from .models.user import CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(Menu)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Period)
admin.site.register(PlateOption)
admin.site.register(Plate)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Adiciona os campos customizados na lista de exibição
    list_display = ['tipo_usuario', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'telefone', 'endereco', 'cpf', 
                    'data_nascimento', 'foto_perfil', 'cnh', 'modelo_moto', 'cor_moto', 'Placa_moto']

    # utilizado para mostrar os novos campos que iram aparecer quando editar um usuario na area administrativa
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Extras', {'fields': ('tipo_usuario', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'foto_perfil', 'cnh', 'modelo_moto', 'cor_moto', 'Placa_moto')}),
    )

    # utilizado para mostrar os novos campos que iram aparecer quando adicionar um novo usuario na area administrativa
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Extras', {'fields': ('tipo_usuario', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'foto_perfil', 'cnh', 'modelo_moto', 'cor_moto', 'Placa_moto')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)