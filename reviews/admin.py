from django.contrib import admin
from . import models

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    
    # "__str__" : 모든 필드 다 보여주나?
    # rating_average는 모델의 함수명
    list_display = ("__str__", "rating_average")
