from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    # 특정 방의, 특정 user가 준 평점 요소(accuracy, cleanliness ..등)의 평균값.
    # 평점의 평균값을 프론트엔드와 어드민에서 갖고 싶어서 model에 연산함수를 넣음.
    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        # 2자리수까지 반올림한 결과값 반환.
        return round(avg, 2)

    # admin패널의 list_display에 등록되어, 보여지는 칼럼명.
    rating_average.short_description = "Avg."