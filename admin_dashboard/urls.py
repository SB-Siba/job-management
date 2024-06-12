from django.urls import path
from . import views

from .credentials import credential
from .manage_product import user,catagory,job


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
    path("user/deleteuser/<int:id>", user.delete_user, name="deleteuser"),
    path('user/user_detail/<int:id>', user.user_detail, name='user_detail'),
    path('edit_user/<int:user_id>',user.Edit_User,name="edit_user"),


    # # catagory web
    path("catagory/catagory_list", catagory.CatagoryList.as_view(), name="catagory_list"),
    path("catagory/catagory_update/<str:catagory_id>", catagory.CatagoryUpdate.as_view(), name="catagory_update"),
    path("catagory/catagory_delete/<str:catagory_id>", catagory.CatagoryDelete.as_view(), name="catagory_delete"),

    # # catagory api
    # path("catagory/catagory_list_api", catagory.CatagotyListApi.as_view()),
    path("catagory_Job_list/<str:catagory_id>", job.CatagoryJobFilter.as_view()),
    path("api_Job_filter", job.ApiJobList.as_view()),
    path("api_Job_detail/<str:Job_uid>", job.ApiJobDetail.as_view()),

    # #product web
    path("job/job_list", job.JobList.as_view(), name="job_list"),
    path("job/job_search", job.JobSearch.as_view(), name="job_search"),
    path("job/job_filter", job.JobFilter.as_view(), name="job_filter"),
    path("job/job_add", job.JobAdd.as_view(), name="job_add"),
    path("job/job_update/<str:job_uid>", job.JobUpdate.as_view(), name="job_update"),
    path("job/job_delete/<str:job_uid>", job.JobDelete.as_view(), name="job_delete"),
    
    # #product_api
    path("catagory_job_list/<str:catagory_id>", job.CatagoryJobFilter.as_view()),
    path("api_job_filter", job.ApiJobList.as_view()),
    path("api_job_detail/<str:job_uid>", job.ApiJobDetail.as_view()),

    

    #credential
    path('credential/add_credential', credential.CreateCredential.as_view(), name="add_credential"),
    path('credential/change_password', credential.Change_password.as_view(), name="change_password"),
    path('credential/change_user_status', credential.UserActiveInactive.as_view(), name="change_user_status"),

    # contact message
    path("contact_messages/all_mesages/",messages.ContactMessageList.as_view(), name="all_contact_message"),
    path("contact_messages/contact_message_detail/<str:uid>",messages.ContactMessageDetail.as_view(), name="contact_message_detail"),
    path("contact_messages/contact_message_reply/<str:uid>",messages.ContactMessagereply.as_view(), name="contact_message_reply"),


]
