from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("v1/mobiles",views.MobileViewSetView,basename="mobiles")

urlpatterns=[
    path("mobiles/",views.MobileListCreateView.as_view()),
    path("mobiles/<int:pk>/",views.MobileUpdateDetailDeleteView.as_view()),
] + router.urls 