from django.views.generic import ListView, DetailView
# from django.shortcuts import render
# from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import Http404
from django_countries import countries
from . import models, forms


#################### RoomDetail과 같은 기능을 하는 FBV
# params)
# request : urls.py를 통해 전달받은 request(uri값)
# potato : urls.py에서 <int:pk>로 넘겨준 값을 가짐. urldispatcher에 의해 분기될 값.
def room_detail(request, pk):
    print("_====================")
    print("pk : " + pk)
    # DB로부터 room데이터 가져오기.
    try:
        room = models.Room.object.get(pk=pk)
        print(room)
        # {"room":room} : "room"이라는 context에 room객체 정보를 담아 프론트 페이지에 전달.
        return render(request, "rooms/dddetail.html", {"room": room})
    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        return Http404()


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


# 세부페이지로 이동하게 하는 CBV임.
# 자동으로 room_detail.html 을 찾아서 반환함....ㄷㄷㄷ
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):

    # form = forms.SearchForm()
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms",0))
    beds = int(request.GET.get("bed", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.get("amenities")
    s_facilities = request.GET.get("facilities")
    print(s_amenities, s_facilities)

    form = {
        "city" : city,
        "s_room_type" : room_type,
        "s_country" : country,
        "price" : price,
        "guests" : guests,
        "bedrooms" : bedrooms,
        "beds" : beds,
        "baths" : baths,
    }

    # room_types = models.RoomType.objects.all()
    # return render(request, "rooms/search.html", {"city": city, "countries" : countries, "room_types" : room_types},)

    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries" : countries,
        "room_types" : room_types,
        "amenities" : amenities,
        "facilities" : facilities,
    }

    return render(request, "rooms/search.html", {**form, **choices})