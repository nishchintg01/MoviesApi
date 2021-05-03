from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register('collection', ColectionsViewset, basename="collection")
router.register('movies',GetMoviesList, basename="movies")

urlpatterns = [
    path('', include(router.urls)),
    path('token/generate', TokenObtainPairView.as_view(), name = "generatetoken"),
    path('token/refresh', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('register', RegisterUsers.as_view(),name = "create-token"),
]
