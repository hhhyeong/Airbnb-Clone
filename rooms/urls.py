from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    # path("<int:potato", views.room_detail, name="detail"),
    # front 페이지에서 사용자에게 입력받는 값을 views.py에 전달.
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]