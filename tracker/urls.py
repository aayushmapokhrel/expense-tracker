from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.views import (
    ExpenseIncomeViewSet,
    UserRegistrationView,
    CustomTokenObtainPairView,
)

router = DefaultRouter()
router.register(r"expenses", ExpenseIncomeViewSet, basename="expenses")

urlpatterns = [
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path(
        "auth/refresh/", CustomTokenObtainPairView.as_view(), name="token_refresh"
    ),
    path("", include(router.urls)),
]
