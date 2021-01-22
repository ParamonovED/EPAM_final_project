from django.urls import path
from . import views

app_name = "ads_checker"
urlpatterns = [
    path("", views.main_page, name="main"),
    path("add_target", views.add_target, name="add_target"),
    path("<int:target_id>/", views.view_target, name="view_target"),
    path("<int:target_id>/poll", views.poll, name="poll"),
    path("<int:target_id>/del", views.delete_target, name="del"),
]
