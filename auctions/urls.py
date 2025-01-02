from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creatlist", views.create_list, name="create_list"),
    path("listings/<int:list_id>", views.list_view, name="list_view"),
    path("listings/<int:list_id>/bid", views.place_bid, name="place_bid"),
    path("listings/<int:list_id>/add_watch_list", views.add_watch_list, name="add_watch_list"),
    path("listings/<int:list_id>/remove_watch_list", views.remove_watch_list, name="remove_watch_list"),
    path("watchlist", views.view_watch_list, name="view_watch_list"),
    path("listings/<int:list_id>/finish_auction", views.finish_auction, name="finish_auction"),
    path("listings/<int:list_id>/add_comment", views.add_comment, name="add_comment"),
    path('category/', views.view_category, name='view_category'),
    path('category/<str:category>/', views.view_category_list, name='view_category_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
