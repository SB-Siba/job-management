from django.urls import path, include
from . import views
from django.contrib import admin
from .credentials import credential
from .manage_product import user,catagory,job,client
from user.views import ApplicationList, DownloadResumeView
from .manage_product.client import  DeleteClientView
from .manage_product.client import ClientUpdateView

# from .order import order
from .contact_messages import messages
app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.AdminDashboard.as_view(), name = "admin_dashboard"),    
    path('privacy_policy_api', views.ApiPrivacyPolicy.as_view(),),
    path('terms_and_conditions', views.ApiTermsCondition.as_view(),),
    path('about_us', views.ApiAbountUs.as_view(),),
    path('admin/', admin.site.urls),
    path('quotation/', include('quotation.urls', namespace='quotation')),
    path('applications/<int:job_id>/', ApplicationList.as_view(), name='application_list'),
    path('applications/download_resume/<int:application_id>/', DownloadResumeView.as_view(), name='download_resume'),

    # Userlist
    path("user/userslist", user.UserList.as_view(), name="user_list"),
    path("user/deleteuser/<int:user_id>", user.DeleteUser.as_view(), name="deleteuser"),
    path('user/user_detail/<int:user_id>', user.UserDetailView.as_view(), name='user_detail'),
    path('edit_user/<int:user_id>',user.Edit_User.as_view(),name="edit_userrr"),
    path('add_user/', user.AddUserView.as_view(), name='add_user'),
    path('employees/', user.EmployeeList.as_view(), name='employee_list'),
    path('employee/<int:employee_id>/', user.EmployeeDetail.as_view(), name='employee_detail'),

    # # category web
    path("category/category_list", catagory.categoryList.as_view(), name="category_list"),
    path('category/category_add/', catagory.categoryAdd.as_view(), name='category_add'),
    path("category/category_update/<str:category_id>", catagory.categoryUpdate.as_view(), name="category_update"),
    path('category_delete/<int:pk>/', catagory.CategoryDeleteView.as_view(), name='category_delete'),
    # # category api
    path('wati-api/', include('wati_api.urls')),

    
    #client list
    path('clients/', client.AdminClientListView.as_view(), name='client_list'),
    path('clients/create/', client.AdminClientCreateView.as_view(), name='client_create'),
    path('client-request/', client.ClientRequestView.as_view(), name='client_request'),
    path('client/<client_id>/', client.ClientDetailView.as_view(), name='client_detail'),
    path('client/edit/<int:uid>/', ClientUpdateView.as_view(), name='edit_client'),
    path('client/delete/<int:client_id>/', DeleteClientView.as_view(), name='delete_client'),

    # #product web
    path("job/job_list/", job.JobList.as_view(), name="job_list"),
    # path('jobs/<int:job_id>/publish/', job.JobPublish.as_view(), name='job_publish'),
    # path('jobs/<int:job_id>/unpublish/', job.JobUnpublish.as_view(), name='job_unpublish'),
    path('applications/', job.ApplicationList.as_view(), name='application_list'),
    path("job/job_search/", job.JobSearch.as_view(), name="job_search"),
    path('job/job_filter/', job.JobFilter.as_view(), name='job_filter'),
    path('job/job_detail/<int:job_uid>/', job.JobDetail.as_view(), name='job_detail'),
    path('job/job_add/', job.JobAdd.as_view(), name='job_add'),
    path('job/edit/<int:job_id>/', job.JobEdit.as_view(), name='job_edit'),
    # path('job/job_update/<int:job_id>/', job.JobUpdate.as_view(), name='job_update'),
    path('job/job_delete/<int:job_uid>/', job.JobDelete.as_view(), name='job_delete'),  
    # #product_api
    

    #credential
    path('credential/add_credential', credential.CreateCredential.as_view(), name="add_credential"),
    path('credential/change_password', credential.Change_password.as_view(), name="change_password"),
    path('credential/change_user_status', credential.UserActiveInactive.as_view(), name="change_user_status"),

    # contact message
    path("contact_messages/all_mesages/",messages.ContactMessageList.as_view(), name="all_contact_message"),
    path("contact_messages/contact_message_detail/<str:uid>/", messages.ContactMessageDetail.as_view(), name="contact_message_detail"),
    path("contact_messages/contact_message_reply/<str:uid>",messages.ContactMessagereply.as_view(), name="contact_message_reply"),




    path('employees/edit/<int:employee_id>/', user.EmployeeEditView.as_view(), name='employee_edit'),
    path('employees/', user.EmployeeList.as_view(), name='employee_list'),
    path('employees/delete/<int:employee_id>/', user.DeleteEmployee.as_view(), name='employee_delete'),
    
] 
