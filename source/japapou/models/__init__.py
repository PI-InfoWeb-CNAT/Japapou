from django.db import models  # type: ignore
from django.contrib.auth.models import User as DjangoUser  # type: ignore
from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore

from .user import User  # type: ignore
from .cardapio import Cardapio  # type: ignore
from .prato import Prato  # type: ignore
from .menu import Menu  # type: ignore
