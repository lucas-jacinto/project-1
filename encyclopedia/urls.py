from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("wiki/newEntry", views.newEntry, name="newEntry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit")
]
