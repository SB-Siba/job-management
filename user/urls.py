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
from .views import ClientJobList
from admin_dashboard.manage_product import user



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
  

    #Page Urls
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('updateprofile/',views.UpdateProfileView.as_view(),name="updateprofile"),    
    path('job/<int:pk>/', views.UserJobDetail.as_view(), name='job_detail'),
    path('user/job-search/', views.UserJobSearch.as_view(), name='job_search'),
    path('user/job-filter/', views.UserJobFilter.as_view(), name='job_filter'),
    path('user/<int:pk>/apply/', views.ApplyForJobView.as_view(), name='job-apply'),
    path('applied-jobs/', views.AppliedJobsView.as_view(), name='applied_jobs'),
    path('application-success/', views.ApplicationSuccess.as_view(), name='application_success'),
    # path('account-details',views.AccountDetails.as_view(),name='account_details'),
    path('sector', views.Sector.as_view(), name = "sector"),
    path('job-opening', views.JobOpening.as_view(), name = "job-opening"),
    path('contactmessage',views.contactMesage.as_view(),name="contactmessage"),
    path('about',views.AboutPage.as_view(),name="about"),
    path('thank-you/',views.ThankYou.as_view(),name='thank_you'),
    
    #client urls
    path('', views.HomeView.as_view(), name='home'),  # This should match the root URL or any relevant path
    path('jobs/', views.ClientJobList.as_view(), name='client_job_list'),
    path('jobs/<int:job_id>/', views.JobDetail.as_view(), name='client_job_detail'),
    path('applications/<int:job_id>/', views.ApplicationList.as_view(), name='application_list'),
    path('employees/<int:job_id>/', views.EmployeeListView.as_view(), name='employee_list'),
    path('all-employees/', views.EmployeeListOverview.as_view(), name='employee_list_overview'),
    path('employee/<int:pk>/', views.EmployeeDetail.as_view(), name='employee_detail'),
    path('new-employees/', views.NewEmployeesView.as_view(), name='new_employees'),
    path('replace-employee/<int:clientemployee_id>/', views.ReplaceEmployeeView.as_view(), name='replace_employee'),
]
