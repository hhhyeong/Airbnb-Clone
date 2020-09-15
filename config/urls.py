from django.contrib import admin
# from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("admin/", admin.site.urls),
]

# 개발 환경에서 "[BASE_URL]/uploads" 경로를 찾아... "/media"랑은 무슨 관련이 있징?.?
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)