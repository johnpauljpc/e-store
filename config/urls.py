
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('estore-admin/', admin.site.urls),
    path('users/', include("users.urls")),
    path("", include("core.urls")),
]
