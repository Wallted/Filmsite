from django.urls import path
from . import views

urlpatterns = [
    path("", views.app_index, name="index"),
    path("home/", views.app_index, name="index"),
    path("movies/<int:pk>/", views.app_movie, name="movie"),
    path("movies/<int:pk>/favourite", views.favourite_movie, name="favourite_movie"),
    path("movies/<int:pk>/cast", views.view_cast, name="cast"),
    path("movies/create/", views.create, name="create"),
    path("movies/<int:pk>/forum/", views.forum, name="forum"),
    path("movies/<int:pk>/forum/page/<int:page>", views.forum, name="forum"),
    path("movies/<int:id>/forum/add/", views.add_thread, name="add_thread"),
    path("movies/thread/<int:id>/", views.view_thread, name="view_thread"),
    path("movies/thread/<int:id>/add", views.add_post, name="add_post"),
    path("actor/<int:id>", views.view_actor, name="view_actor"),
    path("find/", views.find_movie, name="find_movie"),
    path("ranking/", views.view_ranking, name="view_ranking"),
    path("user/", views.view_user, name="view_user"),
    path("profile/<int:id>", views.view_profile, name="view_profile")
]
