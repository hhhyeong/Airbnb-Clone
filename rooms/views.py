from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django_countries import countries
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    # "page_obj" 를 이용하면, page객체로 이용할수있대.
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# 자동으로 room_detail.html 을 찾아서 반환함.
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


class SearchView(View):
    def get(self, request):
        print(request)
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
                qs = models.Room.objects.filter(**filter_args).order_by("-city")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                print(rooms)

            return render(request, "rooms/search.html", {"form":form, "rooms":rooms})
        
        # form에서 사용자가 선택한 값들을 기억하지 못할 경우,
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form":form})
        