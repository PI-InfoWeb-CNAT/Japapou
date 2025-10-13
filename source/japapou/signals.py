from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    '''
        Sinal para adicionar automaticamente usuários a grupos com base no tipo de usuário.
    '''

    if created: # a variavel created é True se o usuário foi criado agora
        # a variavel instance é o usuário que acabou de ser criado
        if instance.tipo_usuario == 'CLIENT':
            group_name = 'Clientes'
        elif instance.tipo_usuario == 'DELIVERY_MAN':
            group_name = 'Entregadores'
        elif instance.tipo_usuario == 'MANAGER':
            group_name = 'Gerentes'
            try:
                group = Group.objects.get(name=group_name)
                instance.groups.add(group)
                print(f"Usuário {instance.username} adicionado ao grupo {group_name}.")
            except Group.DoesNotExist:
                print(f"Grupo {group_name} não existe.")