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
    path('password-reset/', authenticate.CustomPasswordResetView.as_view(),name='password-reset'),
    path('password-reset/done/', authenticate.CustomPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', authenticate.CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',authenticate.CustomPasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('logout', authenticate.Logout.as_view(), name = "logout"),
    # path('forgot-password/',authenticate.ForgotPasswordView.as_view(), name='forgot_password'),
    # path('reset-password/<str:token>/',authenticate.ResetPasswordView.as_view(), name='reset_password'),
    #Page Urls
    path('',views.HomeView.as_view(),name="home"),
    # path('user_view',views.UserDashboard.as_view(),name="user_home"),
    path('profile',views.ProfileView.as_view(),name="profile"),
    path('updateprofile',views.UpdateProfileView.as_view(),name="updateprofile"),
    # path('add_user/',views.ADD_USER,name="add_user"),
    # path('user/jobs', views.UserJobList.as_view(), name='job_list'),
    # path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('user/job-search/', views.UserJobSearch.as_view(), name='job_search'),
    path('user/job-filter/', views.UserJobFilter.as_view(), name='job_filter'),
    path('user/<int:pk>/apply/', views.ApplyForJobView.as_view(), name='job-apply'),
    path('jobs/applied/', views.AppliedJobsView.as_view(), name='applied_jobs'),
    path('application-success/', views.ApplicationSuccess.as_view(), name='application_success'),
    # path('job/<int:pk>/', views.job_detail, name='job_detail'),
    # path('job/<int:pk>/apply/', views.apply_for_job, name='apply_for_job'),
    path('account-details',views.AccountDetails.as_view(),name='account_details'),
    path('sector', views.Sector.as_view(), name = "sector"),
    path('job-opening', views.JobOpening.as_view(), name = "job-opening"),
    path('contactmessage',views.contactMesage.as_view(),name="contactmessage"),
    path('about',views.AboutPage.as_view(),name="about"),
    path('thank-you/',views.ThankYou.as_view(),name='thank_you'),
]