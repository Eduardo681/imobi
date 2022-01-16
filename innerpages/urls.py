from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('immobile/<str:id>', views.immobile, name="immobile"),
    path('schedule', views.schedule, name="schedule"),
    path('schedules', views.schedules, name="schedules"),
    path('cancel/<str:id>', views.cancel, name="cancel")

]
