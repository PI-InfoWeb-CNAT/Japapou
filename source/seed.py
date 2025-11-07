import os
from datetime import date

# Configure Django settings module before importing django modules that access settings
# Use the correct module path (note the capital 'A' in 'japapouAdmin') and choose the
# appropriate settings file (development/production). Here we point to development.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'japapouAdmin.settings.development')

import django
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.conf import settings
from django.core.files import File

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
        perm_view_period = Permission.objects.get(content_type=content_type_period, codename='view_period')

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
    
    print("\n--- GRUPOS CRIADOS COM SUCESSO ---\n")

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

    print("\n--- PERMISSÕES ATRIBUIDAS AOS DETERMINADOS GRUPOS COM SUCESSO ---\n")

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
        
        print("\n--- USUARIOS CRIADOS COM SUCESSO ---\n")
    except Exception as e:
        print(f"Erro ao criar usuarios: {e}")

def criar_menus_periodos():
    print("\nCriando Menus e Períodos...")

    try:
        menu_principal, criado_menu = Menu.objects.get_or_create(
            name="Menu Principal"
        )
        
        if criado_menu:
            print(f"Menu '{menu_principal.name}' criado.")
        else:
            print(f"Menu '{menu_principal.name}' já existia.")
        
        data_inicio = date(2025, 1, 1)
        data_fim = date(2025, 12, 31)

        periodo, criado_periodo = Period.objects.get_or_create(
            menu=menu_principal,
            start_date=data_inicio,
            defaults={'end_date': data_fim} # 'defaults' só usa se for criar
        )

        if criado_periodo:
            print(f"Período de {data_inicio} a {data_fim} criado para o menu.")
        else:
            print("Período já existia.")
        
        print("\n--- MENU E PERIODO CRIADO COM SUCESSO ---\n")
    except Exception as e:
        print(f"ERRO ao criar menus ou períodos: {e}")

def criar_pratos():
    print("criando pratos...")

    try:
        # Usamos .get() para buscar o menu exato que criamos antes
        menu_principal = Menu.objects.get(name="Menu Principal")
    except Menu.DoesNotExist:
        print("ERRO: 'Menu Principal' não foi encontrado.")
        print("Por favor, execute a função 'criar_menus_e_periodos' primeiro.")
        return
    except Exception as e:
        print(f"ERRO ao buscar menu: {e}")
        return

    image_path = os.path.join(settings.BASE_DIR, 'seed_data', 'imgs')

    if not os.path.exists(image_path):
        print(f"\n--- AVISO ---")
        print(f"Imagem placeholder não encontrada em: {image_path}")
        print("O campo 'photo' do Prato é obrigatório (null=False).")
        print("Não é possível criar pratos sem esta imagem de exemplo.")
        print("Por favor, adicione a imagem e execute o script novamente.")
        print("---------------")
        return
    
    try:
        sushi_image_filename = 'sushi.jpg' # Nome do ficheiro da imagem
        sushi_image_path = os.path.join(image_path, sushi_image_filename)

        if not os.path.exists(sushi_image_path):
            print(f"\n--- AVISO: Imagem {sushi_image_filename} não encontrada em {image_path}")
            print("--- Prato 'Sushi' será IGNORADO.")
        
        else:
            plate_sushi, criado_sushi = Plate.objects.get_or_create(
                name="Combinado Sushi Salmão (12pçs)",
                defaults={
                    'price': 45.50,
                    'description': "Delicioso combinado com 6 sashimis, 4 uramakis e 2 niguiris.",
                    'keywords': "sushi, salmao, combinado, peixe cru",
                    # Note: Não passamos a 'photo' aqui nos defaults
                }
            )

            if criado_sushi:
                print(f"Prato '{plate_sushi.name}' criado.")
                # Se o prato foi CRIADO, temos de adicionar a imagem
                with open(sushi_image_path, 'rb') as f:
                    # 'rb' = Read Binary (Modo de leitura binária, necessário para imagens)
                    
                    # Criamos um objeto 'File' do Django
                    django_file = File(f)
                    
                    # O .save() trata de copiar o ficheiro para o seu MEDIA_ROOT
                    plate_sushi.photo.save(sushi_image_filename, django_file, save=True)
                menu_principal.plates.add(plate_sushi)
            else:
                print(f"Prato '{plate_sushi.name}' já existia.")


        yaki_image_filename = 'yakisoba.jpg' # Nome do ficheiro da imagem
        yaki_image_path = os.path.join(image_path, yaki_image_filename)

        if not os.path.exists(yaki_image_path):
            print(f"\n--- AVISO: Imagem {yaki_image_path} não encontrada em {image_path}")
            print("--- Prato 'Yakisoba' será IGNORADO.")
        else:
            plate_yaki, criado_yaki = Plate.objects.get_or_create(
                name="Yakisoba de Carne",
                defaults={
                    'price': 32.00,
                    'description': "Macarrão frito com pedaços de carne e legumes selecionados.",
                    'keywords': "yakisoba, carne, macarrao, legumes",
                }
            )

            if criado_yaki:
                print(f"Prato '{plate_yaki.name}' criado.")
                with open(yaki_image_path, 'rb') as f:
                    django_file = File(f)
                    # Damos um nome de ficheiro diferente para o media
                    plate_yaki.photo.save(yaki_image_filename, django_file, save=True)
                menu_principal.plates.add(plate_yaki)
            else:
                print(f"Prato '{plate_yaki.name}' já existia.")

        
        temaki_image_filename = 'temaki.jpg' # Nome do ficheiro da imagem
        temaki_image_path = os.path.join(image_path, temaki_image_filename)

        if not os.path.exists(temaki_image_path):
            print(f"\n--- AVISO: Imagem {temaki_image_filename} não encontrada em {image_path}")
            print("--- Prato 'Temaki' será IGNORADO.")
        else:
            plate_temaki, criado_temaki = Plate.objects.get_or_create(
                name="Temaki",
                defaults={
                    'price': 15.00,
                    'description': "Temaki de salmão",
                    'keywords': 'temaki',
                }
            )

            if criado_temaki:
                print(f"Prato {plate_temaki.name} criado.")
                with open(temaki_image_path, 'rb') as f:
                    django_file = File(f)
                    plate_temaki.photo.save(temaki_image_filename, django_file, save=True)
                menu_principal.plates.add(plate_temaki)
            else:
                print(f"Prato {plate_temaki.name} já existia.")

        
        onigiri_image_filename = 'onigiri.jpg' # Nome do ficheiro da imagem
        onigiri_image_path = os.path.join(image_path, onigiri_image_filename)

        if not os.path.exists(onigiri_image_path):
            print(f"\n--- AVISO: Imagem {onigiri_image_filename} não encontrada em {image_path}")
            print("--- Prato 'Onigiri' será IGNORADO.")
        else:
            plate_onigiri, criado_onigiri = Plate.objects.get_or_create(
                name="Onigiri",
                defaults={
                    'price': 12.00,
                    'description': "onigiri, bolinho de arroz.",
                    'keywords': 'onigiri, bolinho, arroz'
                }
            )

            if criado_onigiri:
                print(f"Prato {plate_onigiri.name} criado.")
                with open(onigiri_image_path, 'rb') as f:
                    django_file = File(f)
                    plate_onigiri.photo.save(onigiri_image_filename, django_file, save=True)
                menu_principal.plates.add(plate_onigiri)
            else:
                print(f"Prato {plate_onigiri.name} já existia.")

        print("\n--- PRATOS CRIADOS COM SUCESSO ---\n")
    except Exception as e:
        print(f"\nErro inesperado ao criar prato {e}")

if __name__ == "__main__":
    try:
        with transaction.atomic():
            criar_grupos_permissoes()
            criar_users()
            criar_menus_periodos()
            criar_pratos()

            print("\n--- SCRIPT CONCLUÍDO COM SUCESSO ---\n")
    
    except Exception as e:
        print(f"\n--- OCORREU UM ERRO DURANTE A EXECUÇÃO ---")
        print(f"Erro: {e}")
        print("As alterações na base de dados foram revertidas (rollback).")