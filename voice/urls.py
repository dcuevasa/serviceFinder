from django.urls import include, path
from . import views
urlpatterns = [
    path("sendAudio/",views.sendAudio, name="sendAudio"),
    path("",views.home, name="home")
]