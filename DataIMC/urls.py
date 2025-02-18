from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewset, MealViewSet

from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter() 

router.register(r'users', UserViewset) 
router.register(r'meals', MealViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('calculate-bmi/', views.calculate_bmi, name='calculate-bmi'),
    path('bmi-history/', views.bmi_history, name="bmi-history") 
]


