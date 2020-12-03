from math import ceil
from datetime import datetime
from django.shortcuts import render, redirect
from django_countries import countries
from django.urls import reverse
from django.http import Http404
from django.views.generic import ListView, DetailView

# from django.core.paginator import Paginator, EmptyPage
# from django.views.generic import ListView
# from . import models
from . import models, forms


class HomeView(ListView):
    model = models.Room
    pagination_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):
    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    # return render(request, "rooms/search.html", {"city": city})
    room_type = int(request.GET.get("room_type", 0))
    country = request.GET.get("country", "KR")
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    # print(s_amenities, s_facilities)
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.get("amenities")
    s_facilities = request.GET.get("facilities")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # return render(
    #     request,
    #     "rooms/search.html",
    #     # {"city": city, "countries": countries, "room_types": room_types},
    #     {**form, **choices},
    # )

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filte_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html")
#     except models.Room.DoesNotExist:
#         # return redirect(reverse("core:home"))
#         raise Http404()
# print(pk)


# home.html에서 요청받은 page 쪽수에 대하여,
# all_rooms에 room object 10개를 받아와서 home.html에 rendering.
# def all_rooms(request):
#     # return render(request, "all_rooms")
#     # now = datetime.now()
#     # hungry = True
# 모든 Room Model의 objects를 보여주는건 DB를 죽이게 될것! Never.
#     # all_rooms = models.Room.objects.all()
#     # return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})
#     # page = int(request.GET.get("page", 1))
#     # page = int(page or 1)
#     # page_size = 10
#     # limit = page_size * page
#     # offset = limit - page_size
#     # all_rooms = models.Room.objects.all()[offset:limit]
#     # page_count = ceil(models.Room.objects.count() / page_size)
#     # # return render(request, "rooms/home.html", context={"potato": all_rooms})
#     # return render(
#     #     request,
#     #     "rooms/home.html",
#     #     {
#     #         "potato": all_rooms,
#     #         "page": page,
#     #         "page_count": page_count,
#     #         "page_range": range(1, page_count),
#     #     },
#     # )
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")
