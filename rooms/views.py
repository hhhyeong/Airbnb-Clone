from django.views.generic import ListView, DetailView
# from django.shortcuts import render
# from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import Http404
from django_countries import countries
from . import models, forms



# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)

#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page":rooms})
#     except EmptyPage:
#         return redirect


# Django Documentation 참고. abstract 속성을 사용하는 방법 참고 필수!
# CCV(classy class view) 사이트 참고. ListView의 속성이 자세하게 나오지 않아 헷갈릴수있음.
# ListView : 페이지가 objects의 목록을 대변한다.
# 자동으로 "[app_name]_list.html"을 찾아서 반환한다.
# rooms_list.html로 이동.
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    # "page_obj" 를 이용하면, page객체로 이용할수있대.
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


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


# 세부페이지로 이동하게 하는 CBV임.
# 자동으로 room_detail.html 을 찾아서 반환함....ㄷㄷㄷ
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    # form = forms.SearchForm()
    # request로 받은 도시의 정보 가져오기
    # parameter입력 없이 "/rooms/search"로 이동하면,
    # city가 None일 때, input에 기본값"Anywhere" 설정.
    city = request.GET.get("city", "Anykind")
    # if city == '':
    #     city = "Anykind"
    # city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms",0))
    beds = int(request.GET.get("beds", 0))
    print(beds)
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)

    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    print(s_amenities, s_facilities)

    # 선택한 정보
    form = {
        "city" : city,
        # selected room_type
        "s_room_type" : room_type,
        # selected country. 프론트에서 헷갈리지않게 네이밍. 프론트에 넘어가는 변수는 "s_country".
        "s_country" : country,
        "price" : price,
        "guests" : guests,
        "bedrooms" : bedrooms,
        "beds" : beds,
        "baths" : baths,
        "s_amenities" : s_amenities,
        "s_facilities" : s_facilities,
        "instant" : instant,
        "super_host" : super_host

    }

    room_types = models.RoomType.objects.all()
    # return render(request, "rooms/search.html", {"city": city, "countries" : countries, "room_types" : room_types},)
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    # option에 보여줄 선택지 정보.
    choices = {
        "countries" : countries,
        "room_types" : room_types,
        "amenities" : amenities,
        "facilities" : facilities,
    }
    print(form)
    return render(request, "rooms/search.html", {**form, **choices})