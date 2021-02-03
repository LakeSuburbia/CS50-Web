from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sell", views.sell, name="sell"),
    path("<str:product>", views.product, name="product"),
    path("<str:product>/bid", views.bid, name="bid")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
