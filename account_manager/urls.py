from django.urls import path
from . import views
from allauth.account.views import (
    LogoutView, SignupView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView, PasswordSetView
)
from allauth.socialaccount.views import (
    SignupView, 
    LoginCancelledView, 
    LoginErrorView, 
    ConnectionsView,
)
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount.providers.google.provider import GoogleProvider


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='account_login'),
    path('signup/', views.CustomSignupView.as_view(), name='account_signup'),
    path('password/set/', PasswordSetView.as_view(), name='account_set_password'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('password/reset/key/<uidb36>/<key>/', PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/key/done/', PasswordResetFromKeyDoneView.as_view(), name='account_reset_password_from_key_done'),
    path('account_inactive/', views.account_inactive, name='account_inactive'),
    path('activate_account/<uidb64>/<token>/', views.activate_account, name='activate_account'),

    # socialaccount
    path('social/signup/', SignupView.as_view(), name='socialaccount_signup'),
    path('social/login/cancelled/', LoginCancelledView.as_view(), name='socialaccount_login_cancelled'),
    path('social/login/error/', LoginErrorView.as_view(), name='socialaccount_login_error'),
    path('social/connections/', ConnectionsView.as_view(), name='socialaccount_connections'),
]

urlpatterns += default_urlpatterns(GoogleProvider)
