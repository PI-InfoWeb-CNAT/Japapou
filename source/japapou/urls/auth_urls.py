from django.urls import path  # type: ignore
from japapou.views.auth_view import *  # type: ignore


urlpatterns = [
    path("register/", login_register_view, name="login_register"),
    #path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("pagina_protegida/", pagina_protegida, name="pagina_protegida")
    
]