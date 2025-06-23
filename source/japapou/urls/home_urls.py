from django.urls import path  # type: ignore
from django.shortcuts import redirect  # type: ignore
from japapou.views import home_view  # type: ignore

urlpatterns = [
    path("", home_view, name="home"),
]
