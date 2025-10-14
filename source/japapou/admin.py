from django.contrib import admin
from .models.order_item import OrderItem
from .models.order import Order, Order_Pickup,Order_Delivery
from django.contrib import admin  # type: ignore
from japapou.models import *
from .models.user import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm

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
        ('Informações adicionais', {'fields': ('tipo_usuario', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'foto_perfil')}),
        ('Informações de Entregador', {'fields': ('cnh', 'modelo_moto', 'cor_moto', 'Placa_moto')}),
    )

    # utilizado para mostrar os novos campos que iram aparecer quando adicionar um novo usuario na area administrativa
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações adicionais', {'fields': ('tipo_usuario', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'foto_perfil')}),
        ('Informações de Entregador', {'fields': ('cnh', 'modelo_moto', 'cor_moto', 'Placa_moto')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'total', 'created_at')
    ordering = ('-date',)
    readonly_fields = ('created_at', 'altered_at')


@admin.register(Order_Pickup)
class OrderPickupAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'pickup_date', 'total')
    ordering = ('-pickup_date',)
    readonly_fields = ('created_at', 'altered_at')


@admin.register(Order_Delivery)
class OrderDeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'delivery_man', 'dispatch_date', 'delivery_date', 'total')
    list_filter = ('dispatch_date', 'delivery_man')
    ordering = ('-dispatch_date',)
    readonly_fields = ('created_at', 'altered_at')