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
    path("product/<int:productid>", views.product, name="product"),
    path("bid/<int:productid>", views.bid, name="bid"),
    path("deactivateProduct/<int:productid>", views.deactivateProduct, name="deactivateProduct"),
    path("comment/<int:productid>", views.comment, name="comment"),
    path("category/<str:category>", views.category, name="category"),
    path("category", views.category_overview, name="category_overview"),
    path("watchlist", views.watchlist, name="watchlist")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
