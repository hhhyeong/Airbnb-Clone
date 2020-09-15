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
    pass

# Photo
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass