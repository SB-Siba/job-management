from django.urls import path
from . import views

from .credentials import credential
from .manage_product import user,catagory,job,client


# from .order import order
from .contact_messages import messages
app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.AdminDashboard.as_view(), name = "admin_dashboard"),    
    path('privacy_policy_api', views.ApiPrivacyPolicy.as_view(),),
    path('terms_and_conditions', views.ApiTermsCondition.as_view(),),
    path('about_us', views.ApiAbountUs.as_view(),),

    # Userlist
    path("user/userslist", user.UserList.as_view(), name="userslist"),
    path("user/deleteuser/<int:user_id>", user.DeleteUser.as_view(), name="deleteuser"),
    path('user/user_detail/<int:user_id>', user.UserDetailView.as_view(), name='user_detail'),
    path('edit_user/<int:user_id>',user.Edit_User.as_view(),name="edit_userrr"),
    path('add_user/', user.AddUserView.as_view(), name='add_user'),
    # path('candidates/', user.candidate_list, name='candidates'),
    # path('candidates/<int:candidate_id>/', user.candidate_detail, name='candidate_detail'),
    # path('candidates/<int:candidate_id>/assign_category/', user.assign_category, name='assign_category'),
    # # path('candidates/send_message/', views.send_message, name='send_message'),
    # path('candidates/<int:candidate_id>/update_status_hired/', user.update_status_hired, name='update_status_hired'),
    # # catagory web
    path("catagory/catagory_list", catagory.CatagoryList.as_view(), name="catagory_list"),
    path('catagory/catagory_add/', catagory.CatagoryAdd.as_view(), name='catagory_add'),
    path("catagory/catagory_update/<str:catagory_id>", catagory.CatagoryUpdate.as_view(), name="catagory_update"),
    path("catagory/catagory_delete/<str:catagory_id>", catagory.CatagoryDelete.as_view(), name="catagory_delete"),

    # # catagory api
    
    #client list
    path('clients/', client.AdminClientListView.as_view(), name='client_list'),
    path('clients/create/', client.AdminClientCreateView.as_view(), name='client_create'),
    path('client/<client_id>/', client.ClientDetailView.as_view(), name='client_detail'),

    # #product web
    path("job/job_list/", job.JobList.as_view(), name="job_list"),
    # path('jobs/<int:job_id>/publish/', job.JobPublish.as_view(), name='job_publish'),
    # path('jobs/<int:job_id>/unpublish/', job.JobUnpublish.as_view(), name='job_unpublish'),
    path('applications/', job.ApplicationList.as_view(), name='application_list'),
    path("job/job_search/", job.JobSearch.as_view(), name="job_search"),
    path('job/job_filter/', job.JobFilter.as_view(), name='job_filter'),
    path('job/job_detail/<int:job_uid>/', job.JobDetail.as_view(), name='job_detail'),
    path('job/job_add/', job.JobAdd.as_view(), name='job_add'),
    path('job/<int:job_id>/edit/', job.JobEdit.as_view(), name='job_edit'),

    # path('job/job_update/<int:job_id>/', job.JobUpdate.as_view(), name='job_update'),
    path('job/job_delete/<int:job_uid>/', job.JobDelete.as_view(), name='job_delete'),
    # #product_api
    

    

    #credential
    path('credential/add_credential', credential.CreateCredential.as_view(), name="add_credential"),
    path('credential/change_password', credential.Change_password.as_view(), name="change_password"),
    path('credential/change_user_status', credential.UserActiveInactive.as_view(), name="change_user_status"),

    # contact message
    path("contact_messages/all_mesages/",messages.ContactMessageList.as_view(), name="all_contact_message"),
    path("contact_messages/contact_message_detail/<str:uid>",messages.ContactMessageDetail.as_view(), name="contact_message_detail"),
    path("contact_messages/contact_message_reply/<str:uid>",messages.ContactMessagereply.as_view(), name="contact_message_reply"),
]
