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
    # html 소스 보면 테이블 태그임 (<th><tr> 등).
    # form = forms.SearchForm(request.GET)
    # <p>태그로 변환.
    # form = form.as_p()

    country = request.GET.get("country")
    print(country)

    # 사용자가 입력한 country값을 form이 기억하고 있을 경우.
    if country:
        # bounded form 반환.
        # GET으로 받은 모든 정보를 다 form에게 전달.
        form = forms.SearchForm(request.GET)
        # 폼에서 아무런 에러(유효성 검사 등..)가 없다면 실행.
        if form.is_valid():
            # 폼에서 정리된 데이터를 가져올수있음.
            print(form.cleaned_data)
            # city = form.cleaned_data["city"]
            city = form.cleaned_data.get("city")
            print(city)
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            beds = form.cleaned_data.get("beds")
            bedrooms = form.cleaned_data.get("bedrooms")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type__pk"] = room_type
            
            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if beds is not None:
                filter_args["beds__gte"] == beds

            if baths is not None:
                filter_args["baths__gte"] == baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            for amenity in amenities:
                filter_args["amenities"] = amenity
            
            for facility in facilities:
                filter_args["facilities"] = facility
            print(filter_args)
            rooms = models.Room.objects.filter(**filter_args)
    # form에서 사용자가 선택한 값들을 기억하지 못할 경우,
    else:
        # unbounded form 반환.
        # country가 없으면 유효성검사 할필요 없음.
        form = forms.SearchForm()

    # print(form)
    print(rooms)
    return render(request, "rooms/search.html", {"form":form, "rooms":rooms})