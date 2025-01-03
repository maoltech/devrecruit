# from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from .serializers import (
    SignUpSerializer, ForgotPasswordSerializer, ResetPasswordSerializer,
    WalletSerializer, WalletTransactionSerializer, CreditDebitSerializer
)
from .models import Wallet, WalletTransaction
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpView(APIView):
    @swagger_auto_schema(
        request_body=SignUpSerializer,
        responses={
            201: openapi.Response('User created successfully', SignUpSerializer),
            400: 'Bad request with validation errors'
        }
    )
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SignInView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                        }
                    )
                }
            )),
            401: 'Invalid credentials'
        }
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_object_or_404(User, email=email)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # Send reset email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: /reset/{uidb64}/{token}/",
                from_email="noreply@example.com",
                recipient_list=[email],
            )
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if PasswordResetTokenGenerator().check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Invalid UID."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = get_object_or_404(Wallet, user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WalletCreditView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreditDebitSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            wallet = get_object_or_404(Wallet, user=request.user)
            wallet.balance += amount
            wallet.save()
            WalletTransaction.objects.create(wallet=wallet, transaction_type='credit', amount=amount)
            return Response({"message": "Amount credited successfully", "new_balance": wallet.balance})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletDebitView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreditDebitSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            wallet = get_object_or_404(Wallet, user=request.user)
            if wallet.balance < amount:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            wallet.balance -= amount
            wallet.save()
            WalletTransaction.objects.create(wallet=wallet, transaction_type='debit', amount=amount)
            return Response({"message": "Amount debited successfully", "new_balance": wallet.balance})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = get_object_or_404(Wallet, user=request.user)
        transactions = wallet.transactions.all()
        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data)
