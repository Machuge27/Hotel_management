# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.room_list, name='room_list'),
#     path('book/<int:room_id>/', views.book_room, name='book_room'),
# ]

from django.urls import path, include
from . import views

urlpatterns = [
    path('room_listing', views.room_listing, name='room_listing'),
    path('api/book-room/', views.book_room, name='book_room'),
    path('api/available-rooms/', views.available_rooms, name='available_rooms'),
    path('api/check_availability/', views.check_availability, name='check_availability'),
    path('api/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('accounts/', include('django.contrib.auth.urls')),
]
