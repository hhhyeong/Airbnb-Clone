from django.db import models

# Create your models here.

# 추상모델
class TimeStampedModel(models.Model):
    """ Time Stamped Definition """

    # https://tomining.tistory.com/145
    ### DateTimeField의 속성)
    # 생성 일자    - 최초 등록시에만 저장, 갱신되지 않는 정보.
    #              => auto_now_add=True 사용
    #                 (django model이 최초 저장(insert) 시에만 현재날짜(date.today())를 적용.)
    # 최종 수정일자 - 수정시 갱신.
    #              => auto_now=True 사용
    #                 (django model이 save될때마다 현재날짜(date.today())로 갱신됨.)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
