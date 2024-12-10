# Register your models here.
from django.contrib import admin
from .models import Room, Booking, Customer, Message

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Message)