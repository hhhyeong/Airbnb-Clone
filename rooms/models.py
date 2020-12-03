from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models

# import 할 model들이 많아지면 불편하니까, import도 안하고, String으로 모델을 써줘도 장고는 해당하는 model을 불러옴.
# from users import models as user_models


# 추상모델
class AbstractItem(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# AbstractItem을 상속받을 Type 모델들(RoomType, Amenity, Facility, HouseRule)
class RoomType(AbstractItem):
    class Meta:
        verbose_name = "Room Type"
        # ordering = ["-created"]


class Amenity(AbstractItem):
    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

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
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # 다른 앱의 모델과의 관계를 나타낼 때,
    # import하는 대신 "[앱이름].[모델클래스명]" 이렇게 나타낼 수도 있음!
    # => why?
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # ManyToManyField
    # ForeingKey
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    # #8.8 Intercepting Model save() and admin_save()어느곳을 통해서도 model의 값이 저장될 때 호출되는 함수임.
    # admin패널뿐만 아니라, view, admin, 어느곳을 통해서도 model의 값이 저장될 때 호출되는 함수임.
    # ex) admin패널을 통해 self.city에 새로 입력한 값으로 모델이 바뀌는 기능.
    # admin.py에서도 object값이 바뀔때 호출되도록 하는 save_model()함수가 있음.(누가 저장했는지 알 수 있음.)
    # models.py의 save()함수와 용도가 다름.
    # => 저장 시, 입력값의 앞글자가 대문자로 바뀌어 저장됨.()
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        print(self.city)
        super().save(*args, **kwargs)

    # get_absolute_url() : admin페이지의 세부내용 화면에 "View on site" 버튼 누르면 무조건 이동하는 경로 지정 가능.
    # ex) return "photato"
    # reverse : url name 입력하면 redirect해주는 함수. url에 argument가 필요하다면 추가.
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # 각 room에 대하여, 모든 평균평점값(Avg.)의 평균값을 연산하는 함수.
    # 프론트엔드에서도 각 Room에 대한 평균평점이 보여지기 때문에, models.py에 작성함.
    # reviews모델의 room필드가 related_name으로 "reviews"를 갖기 때문에,
    # room모델에서 self.reviews를 통해 reviews값에 접근 가능.
    # 1개의 room에 대한 평균평점값뿐만 아니라 각 review항목(accuracy average, communication avg, cleaned avg 등)에 대해서도 접근 가능.
    def total_rating(self):
        all_reviews = self.reviews.all()
        # all_ratings = []
        # for review in all_reviews:
        #     all_ratings.append(review.rating_average())
        # return 0
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                # 각 room 객체와 연결된 reviews객체들의 값을 모두 가져와서, 더해줌.
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews))
        return 0