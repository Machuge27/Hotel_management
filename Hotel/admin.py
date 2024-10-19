# Register your models here.
from django.contrib import admin
from .models import Room, Booking, Customer

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Customer)