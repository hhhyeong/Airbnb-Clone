from django.urls import path
from rooms import views as room_views

app_name = "core"

# rooms.views 대신에 rooms_views 를 통해 rooms application을 자동으로 찾아가는건가??
# FBV를 통해 이동
# urlpatterns = [path("", room_views.all_rooms, name="home")]
# CBV를 통해 이동
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]