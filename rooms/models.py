from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
# from users import models as user_models


# 추상모델
class AbstractItem(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)

    class Meta:
        abstract=True

    def __str__(self):
        return self.name


# AbstractItem을 상속받을 Type 모델들(RoomType, Amenity, Facility, HouseRule)
class RoomType(AbstractItem):
    pass

class Amenity(AbstractItem):
    pass


class Facility(AbstractItem):
    pass


class HouseRule(AbstractItem):
    pass


class Photo(core_models.TimeStampedModel):

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

# Create your models here.
class Room(core_models.TimeStampedModel):

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # 다른 앱의 모델과의 관계를 나타낼 때,
    # import하는 대신 "[앱이름].[모델클래스명]" 이렇게 나타낼 수도 있음!
    # => why?
    host = models.ForeignKey("users.User", related_name="rooms", on_delete=models.CASCADE)
    # ManyToManyField
    # ForeingKey
    room_type = models.ForeignKey("RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name