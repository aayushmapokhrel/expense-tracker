from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from tracker.models import ExpenseIncome
from tracker.serializers import (
    ExpenseIncomeSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from tracker.permissions import IsOwnerOrSuperuser


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseIncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all()
        return ExpenseIncome.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
