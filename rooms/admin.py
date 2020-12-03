from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# Room Type, Facility, Amenity, HouseRule
# => ItemAdmin에 등록된 모델들은 추상모델을 상속받아서 모두 DB에 테이블로 추가되는 대상이 아닌 애들인가봄!
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("name", "used_by")

    # Item을 사용하고 있는 Room의 개수?
    def used_by(self, obj):
        return obj.rooms.count()


# #8.6) Inline Admin : admin.TabularInline 상속을 통해,
# rooms>admin.py안에 PhotoAdmin의 기능을 넣음.
# => rooms의 admin패털에서 photos를 추가 가능.
# RoomAdmin 클래스에서 inlines 속성에 추가하네.
class PhotoInline(admin.TabularInline):
    # 생성하고자 하는 Inline admin의 모델값 설정.
    model = models.Photo


# Room
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    # inline admin으로 나타낼 Admin 적기.(여러개 가질 수 있음.)
    inlines = (PhotoInline,)

    # admin panel의 상세페이지 UI
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        # 아코디언 효과
        (
            "More About the Space",
            # {
            #     "classes": ("collapse",),
            #     "fields": ("amenities", "facilities", "house_rules"),
            # },
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    # admin panel의 목록 화면 UI
    # admin.py에서 만든 함수명도, models.py에서 만든 함수명도 컬럼명으로 보여주기 가능.
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # admin패널에서 users목록이 엄청 길어질 경우, 작은 user admin을 띄워서 필터링/검색 가능함.
    raw_id_fields = ("host",)

    search_fields = ("=city", "^host__username")

    # 기존 ManyToMany Field UI에서 추가하기 위한 창에서 검색기능 추가됨.
    filter_horizontal = ("amenities", "facilities", "house_rules")

    def save_model(self, request, obj, form, change):
        print(obj, change, form)
        super().save_model(request, obj, form, change)

    # admin panel의 목록에 보여지는 컬럼에 연산 함수도 추가 가능.
    # queryset 사용) Amenity 객체의 개수 반환.
    def count_amenities(self, obj):
        print(obj)
        return obj.amenities.count()

    count_amenities.short_description = "Amenity Count"

    # queryset 사용) Photo 객체의 개수 반환.
    #               => models.Photo 를 상속한것도 아닌데, Photo모델을 받을수 있나보지???
    #                  obj가 어떤의미일까. models.py 전부를 말하는걸까????
    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


# Photo
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"