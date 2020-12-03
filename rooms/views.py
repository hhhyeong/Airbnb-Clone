from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models, forms


#################### RoomDetail과 같은 기능을 하는 FBV
# params)
# request : urls.py를 통해 전달받은 request(uri값)
# potato : urls.py에서 <int:pk>로 넘겨준 값을 가짐. urldispatcher에 의해 분기될 값.
def room_detail(request, pk):
    print("_====================")
    print(pk)
    # DB로부터 room데이터 가져오기.
    room = models.Room.object.get(pk=pk)
    print(room)
    # {"room":room} : "room"이라는 context를 프론트 페이지에 전달.
    return render(request, "rooms/detail.html", {"room": room})


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    # def room_detail(request, pk):
    #     # print(pk)
    #     # return render(request, "rooms/detail.html")
    #     try:
    #         room = models.Room.objects.get(pk=pk)
    #         return render(request, "rooms/detail.html", {"room": room})
    #     except models.Room.DoesNotExist:
    #         return redirect(reverse("core:home"))


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):

    # form = forms.SearchForm()
    city = request.GET.get("city")
    city = str.capitalize(city)

    return render(request, "rooms/search.html", {"city": city})