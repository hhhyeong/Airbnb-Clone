from django.contrib import admin
from . import models
# Register your models here.


# Room Type, Facility, Amenity, HouseRule
# => ItemAdmin에 등록된 모델들은 추상모델을 상속받아서 모두 DB에 테이블로 추가되는 대상이 아닌 애들인가봄!
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    pass


# Room
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    # admin panel의 상세페이지 UI
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        # 아코디언 효과
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )


    # admin panel의 목록 화면 UI
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

    search_fields = ("=city", "^host__username")

    # 기존 ManyToMany Field UI에서 추가하기 위한 창에서 검색기능 추가됨.
    filter_horizontal = ("amenities", "facilities", "house_rules")


    # admin panel의 목록에 보여지는 컬럼에 연산 함수도 추가 가능.
    def count_amenities(self, obj):
        return obj.amenities.count()



# Photo
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass