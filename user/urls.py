from django.urls import path
from . import views,authenticate
from .forms import PasswordChangeForm
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.auth import views as auth_view

app_name = 'user'

urlpatterns = [
    #Authentication urls
    path('login', authenticate.Login.as_view(), name = "login"),
    path('signup', authenticate.Registration.as_view(), name = "signup"),
    path("passwordChange/",auth_view.PasswordChangeView.as_view(template_name = 'user/authtemp/changepassword.html',form_class = PasswordChangeForm,success_url = '/passwordchangedone'),name='passwordchange'),
    path("passwordchangedone/",auth_view.PasswordChangeDoneView.as_view(template_name = 'user/authtemp/changepassworddone.html'),name='passwordchangedone'),
    path('password-reset/', PasswordResetView.as_view(template_name='user/authtemp/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/authtemp/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='user/authtemp/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='user/authtemp/password_reset_complete.html'),name='password_reset_complete'),
    path('logout', authenticate.Logout.as_view(), name = "logout"),
    
    #Page Urls
    path('',views.HomeView.as_view(),name="home"),
    path('profile',views.ProfileView.as_view(),name="profile"),
    path('updateprofile',views.UpdateProfileView.as_view(),name="updateprofile"),
    # path('add_user/',views.ADD_USER,name="add_user"),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/<int:pk>/apply/', views.apply_for_job, name='apply_for_job'),
    path('account-details',views.AccountDetails.as_view(),name='account_details'),
    path('contactmessage',views.contactMesage.as_view(),name="contactmessage"),
    path('about',views.AboutPage.as_view(),name="about"),
    path('thank-you/',views.ThankYou.as_view(),name='thank_you'),
]