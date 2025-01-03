from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignUpView, SignInView, ForgotPasswordView, ResetPasswordView
from .views import WalletView, WalletCreditView, WalletDebitView, WalletTransactionsView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('signin', SignInView.as_view(), name='signin'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset_password'),
    path('wallet', WalletView.as_view(), name='wallet'),
    path('wallet/credit', WalletCreditView.as_view(), name='wallet_credit'),
    path('wallet/debit', WalletDebitView.as_view(), name='wallet_debit'),
    path('wallet/transactions', WalletTransactionsView.as_view(), name='wallet_transactions'),
]

