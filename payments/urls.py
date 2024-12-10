
from django.urls import path
from . import views

urlpatterns = [
    path("initialize_payment/", views.initialize_payment, name="initialize payment"),
    path("callback/", views.callback, name="Callback fxn"),
]
