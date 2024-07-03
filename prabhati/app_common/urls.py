from django.urls import path
from . import views

from . import authentication
from .contact import contact
app_name = 'app_common'

urlpatterns = [
    path('', views.Login.as_view(), name = "login"),
    path('logout', views.Logout.as_view(), name = "logout"),
    path('delete_account', views.DeleteAccount.as_view(), name='delete_account'),
    path('privacy_policy', views.PrivacyPolicy.as_view(), name='privacy_policy'),


    #authentication api
    path("api/signup",authentication.SignupApi.as_view()),
    path("api/login", authentication.Login.as_view()),
    path("api/forgot_password",authentication.ForgetPassword.as_view()),
    path("api/logout", authentication.LogOut.as_view()),
    #authentication api web_view
    path("new_password_set/<str:encoded_user_id>/<str:otp>", authentication.NewPassword.as_view(), name='new_password_set'),

]