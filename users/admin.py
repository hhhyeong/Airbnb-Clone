from django.contrib import admin

# Admin customizing 클래스
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    # admin페이지의 User 상세 정보에서 파랑색 한블록을 나타냄.
    # models.py의 AbstractUser클래스에서 제공하는 fields와 새로 만들었던 fields도 보여주도록.
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    # 설명필요.
    list_filter = UserAdmin.list_filter + ("superhost",)


    # 엥. is_staff, is_superhost함수 models.py에 왜 추가 안함?
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "language",
        "currency",
        "superhost",
        # "is_staff",
        # "is_superhost"
    )
