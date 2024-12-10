# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.room_list, name='room_list'),
#     path('book/<int:room_id>/', views.book_room, name='book_room'),
# ]

from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views
from .serializers import CustomTokenObtainPairView

urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("room_listing/", views.room_listing, name="room_listing"),
    path("api/book-room/", views.book_room, name="book_room"),
    path("api/delete_booking/", views.delete_booking, name="delete booking"),
    path("api/available-rooms/", views.available_rooms, name="available_rooms"),
    path(
        "api/check_availability/", views.check_availability, name="check_availability"
    ),
    path("api/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("auth/signup/", views.signUp, name="signup"),
    path("auth/signin/", views.signIn, name="signin"),
    path("api/send-message/", views.send_message, name="send_message"),
    path("api/logout/", views.logout, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("payments/", include("payments.urls")),
]
