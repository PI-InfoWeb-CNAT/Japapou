from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("", home_view, name="home"),
    path("contact/", contact_view, name="contact"),
    path("login/", visitor_login_register_view, name="visitor_login"),
    path("menu/", visitor_menu_view, name="visitor_menu"),
]
