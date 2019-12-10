from django.urls import path, include
from rest_framework.routers import DefaultRouter

from demo.core.api.views import AccountViewSet

router = DefaultRouter()

router.register('accounts', AccountViewSet, basename='account')

urlpatterns = [
    path('', include(router.urls))
]
