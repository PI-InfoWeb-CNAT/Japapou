import os
import django
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'japapouadmin.settings.settings')
django.setup()

try:
    from japapou.models import Menu, Plate, Period, CustomUser, Cart, OrderItem, Order, PlateReview, CourierReview
except ImportError:
    print("Não foi possivel encontrar as models, MENU, PLATE, PERIOD e CUSTOMUSER")
    exit()



def criar_grupos_permissoes():
    print("A criar grupos e atribuir permissões...")

    try:
        content_type_plate = ContentType.objects.get_for_model(Plate)
        content_type_menu = ContentType.objects.get_for_model(Menu)
        content_type_period = ContentType.objects.get_for_model(Period)
        content_type_customuser = ContentType.objects.get_for_model(CustomUser)
        content_type_cart = ContentType.objects.get_for_model(Cart)
        content_type_order = ContentType.objects.get_for_model(Order)
        content_type_order_item = ContentType.objects.get_for_model(OrderItem)
        content_type_plate_review = ContentType.objects.get_for_model(PlateReview)
        content_type_courier_review = ContentType.objects.get_for_model(CourierReview)

        perm_add_plate = Permission.objects.get(content_type=content_type_plate, codename='add_plate')
        perm_change_plate = Permission.objects.get(content_type=content_type_plate, codename='change_plate')
        perm_delete_plate = Permission.objects.get(content_type=content_type_plate, codename='delete_plate')
        perm_view_plate = Permission.objects.get(content_type=content_type_plate, codename='view_plate')

        perm_add_menu = Permission.objects.get(content_type=content_type_menu, codename='add_menu')
        perm_change_menu = Permission.objects.get(content_type=content_type_menu, codename='change_menu')
        perm_delete_menu = Permission.objects.get(content_type=content_type_menu, codename='delete_menu')
        perm_view_menu = Permission.objects.get(content_type=content_type_menu, codename='view_menu')

        perm_add_period = Permission.objects.get(content_type=content_type_period, codename='add_period')
        perm_change_period = Permission.objects.get(content_type=content_type_period, codename='change_period')
        perm_delete_period = Permission.objects.get(content_type=content_type_period, codename='delete_period')
        perm_view_period = Permission.objects.get(content_type=content_type_period, codename='add_period')

        perm_add_customuser = Permission.objects.get(content_type=content_type_customuser, codename='add_customuser')
        perm_change_customuser = Permission.objects.get(content_type=content_type_customuser, codename='change_customuser')
        perm_delete_customuser = Permission.objects.get(content_type=content_type_customuser, codename='delete_customuser')
        perm_view_customuser = Permission.objects.get(content_type=content_type_customuser, codename='view_customuser')

        perm_view_cart = Permission.objects.get(content_type=content_type_cart, codename='view_cart')

        perm_view_order = Permission.objects.get(content_type=content_type_order, codename='view_order')
        perm_add_order = Permission.objects.get(content_type=content_type_order, codename='add_order')

        perm_view_order_item = Permission.objects.get(content_type=content_type_order_item, codename='view_orderitem')
        perm_add_order_item = Permission.objects.get(content_type=content_type_order_item, codename='add_orderitem')

        perm_add_plate_review = Permission.objects.get(content_type=content_type_plate_review, codename='add_platereview')
        perm_delete_plate_review = Permission.objects.get(content_type=content_type_plate_review, codename='delete_platereview')
        perm_view_plate_review = Permission.objects.get(content_type=content_type_plate_review, codename='view_platereview')

        perm_add_courier_review = Permission.objects.get(content_type=content_type_courier_review, codename='add_courierreview')
        perm_view_courier_review = Permission.objects.get(content_type=content_type_courier_review, codename='view_courierreview')
        perm_delete_courier_review = Permission.objects.get(content_type=content_type_courier_review, codename='delete_courierreview')

    except ContentType.DoesNotExist:
        print("\nERRO: ContentType para os modelos solicitados não encontrados.")
        print("Verifica se executou o comando 'migrate'")
        return
    
    except Permission.DoesNotExist:
        print("\nERRO: Permissões para os modelos solicitados não encontrados.")
        return
    

    gerentes, criado = Group.objects.get_or_create(name="Gerentes")
    if criado:
        print("Grupo Gerentes criado\n")

    entregadores, criado = Group.objects.get_or_create(name="Entregadores")
    if criado:
        print("Grupo Entregadores criado\n")

    clientes, criado = Group.objects.get_or_create(name="Clientes")
    if criado:
        print("Grupo Clientes criado\n")

    print("\nAtribuindo Permissões...\n")

    permissoes_gerente = [
        # permissoes sobre avaliações
        perm_add_plate_review,
        perm_delete_plate_review,
        perm_view_plate_review,
        perm_add_courier_review,
        perm_view_courier_review,
        perm_delete_courier_review,

        # permissoes sobre usuarios
        perm_add_customuser,
        perm_delete_customuser,
        perm_change_customuser,
        perm_view_customuser,

        # permissoes sobre pratos
        perm_add_plate,
        perm_delete_plate,
        perm_view_plate,
        perm_change_plate,

        # permissoes sobre menus
        perm_add_menu,
        perm_view_menu,
        perm_change_menu,
        perm_delete_menu,

        # permissoes sobre periodos
        perm_add_period,
        perm_view_period,
        perm_change_period,
        perm_delete_period,

        # permissões sobre pedidos
        perm_view_order,
        perm_view_order_item,
    ]

    permissoes_entregadores = [
        # permissoes sobre avaliações
        perm_view_courier_review,
        perm_view_plate_review,
        
        # permissoes sobre usuarios
        perm_change_customuser,
        perm_view_customuser,

        # permissões sobre pedidos
        perm_view_order,
        perm_view_order_item,
    ]

    permissoes_clientes = [
        # permissoes sobre avaliações
        perm_add_plate_review,
        perm_view_plate_review,
        perm_add_courier_review,
        perm_view_courier_review,

        # permissoes sobre usuarios
        perm_change_customuser,
        perm_view_customuser,

        # permissoes sobre pratos
        perm_view_plate,

        # permissoes sobre menus
        perm_view_menu,

        # permissões sobre pedidos
        perm_view_order,
        perm_add_order,
        perm_view_order_item,
        perm_add_order_item,

        # permissões sobre carrinho
        perm_view_cart,

    ]

    gerentes.permissions.set(permissoes_gerente)
    entregadores.permissions.set(permissoes_entregadores)
    clientes.permissions.set(permissoes_clientes)

    print("Permissões atribuídas aos grupos com sucesso.")

def criar_users():
    """Criar usuarios, gerente, cliente e entregador. o admin do site também"""

    try:
        if not CustomUser.objects.filter(username="admin").exists():
            CustomUser.objects.create_superuser(
                username="admin",
                email="",
                password="japapou",
                tipo_usuario="MANAGER",
            )
            print("\nUsuario admin criado com sucesso.\n")
        else:
            print("\nUsuario admin ja existe.\n")

        if not CustomUser.objects.filter(username="usuariogerente").exists():
            CustomUser.objects.create_user(
                username="usuariogerente",
                email="",
                password="@Gerente123",
                tipo_usuario="MANAGER",

                is_staff=False,
                is_superuser=False,
            )
        else:
            print("\nUsuario gerente ja existe.\n")

        if not CustomUser.objects.filter(username="usuariocliente").exists():
            CustomUser.objects.create_user(
                username="usuariocliente",
                email="",
                password="@Cliente123",
                tipo_usuario="CLIENT",

                is_staff=False,
                is_superuser=False,
            )
        else:
            print("\nUsuario Cliente ja existe.\n")

        if not CustomUser.objects.filter(username="usuarioentregador").exists():
            CustomUser.objects.create_user(
                username="usuarioentregador",
                email="",
                password="@Entregador123",
                tipo_usuario="DELIVERY_MAN",

                is_staff=False,
                is_superuser=False,
            )
        else:
            print("\nUsuario Entregador ja existe.\n")
        
        print("\nUSUARIOS CRIADOS COM SUCESSO\n")
    except Exception as e:
        print(f"Erro ao criar usuarios: {e}")

    

def criar_menus():
    pass

def criar_pratos():
    pass
