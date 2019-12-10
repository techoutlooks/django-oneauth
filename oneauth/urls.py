from django.conf.urls import url
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from oneauth import views as one_views
from . import views


# ========== Endpoints [Auth]
urlpatterns = [
    # path('o/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('o/token/', one_views.OneTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('o/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

# ========== Endpoints [User]
router = DefaultRouter()
router.register('users', one_views.OneUserViewSet, base_name='user')
router.register('permissions', one_views.OnePermissionViewSet, basename='permission')
router.register('roles', one_views.OneRoleViewSet, basename='role')


urlpatterns += [
    path('', include(router.urls)),
    path('signup/', views.SignUp.as_view(), name='signup'),
]

