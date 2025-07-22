from django.db import models  # type: ignore
from django.contrib.auth.models import User as DjangoUser  # type: ignore
from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore

from .menu import Menu
from .period import Period
from .plate import Plate
from .user import User
