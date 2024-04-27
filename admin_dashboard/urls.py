from django.urls import path
from . import views

from .credentials import credential
from .manage_product import catagory, product, coupon,episodes,subscription,user
from .order import order
from .contact_messages import messages
app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.AdminDashboard.as_view(), name = "admin_dashboard"),
    # path('banner_list', views.BannerList.as_view(), name = "web_banner_list"),
    # path('banner_delete/<str:banner_id>', views.BannerDelete.as_view(), name = "web_banner_delete"),
    # path('banner_list_api', views.ApiBannerList.as_view(),),

    # privacy policy and terms and about us   
    path('privacy_policy_api', views.ApiPrivacyPolicy.as_view(),),
    path('terms_and_conditions', views.ApiTermsCondition.as_view(),),
    path('about_us', views.ApiAbountUs.as_view(),),

    # Userlist
    path("user/userslist", user.UserList.as_view(), name="userslist"),
    path("user/deleteuser/<int:id>", user.delete_user, name="deleteuser"),


    #Episodes
    path("episode/episode_list", episodes.EpisodeList.as_view(), name="episode_list"),
    path("episode/episode_search", episodes.EpisodeSearch.as_view(), name="episode_search"),
    path("episode/episode_add", episodes.EpisodeAdd.as_view(), name="episode_add"),
    path("episode/episode_update/<str:episode_id>", episodes.EpisodeUpdate.as_view(), name="episode_update"),
    path("episode/episode_delete/<str:episode_id>", episodes.EpisodeDelete.as_view(), name="episode_delete"),


    #Subscription Plan
    path("subscriptionplan/subscriptionplan_list", subscription.SubscriptionPlanList.as_view(), name="subscriptionplan_list"),
    path("subscriptionplan/subscriptionplan_add", subscription.SubscriptionPlanAdd.as_view(), name="subscriptionplan_add"),
    path("subscriptionplan/subscriptionplan_update/<str:subscriptionplan_id>", subscription.SubscriptionPlanUpdate.as_view(), name="subscriptionplan_update"),
    path("subscriptionplan/subscriptionplan_delete/<str:subscriptionplan_id>", subscription.SubscriptionPlanDelete.as_view(), name="subscriptionplan_delete"),
    path("subscriptionplan/subscriptionuserlist", subscription.SubscriptionUserList.as_view(), name="subscriptionuserlist"),



    #SUbscription Feature
    path("subscriptionfeature/subscriptionfeature_list", subscription.SubscriptionFeatureList.as_view(), name="subscriptionfeature_list"),
    path("subscriptionfeature/subscriptionfeature_add", subscription.SubscriptionFeatureAdd.as_view(), name="subscriptionfeature_add"),
    path("subscriptionfeature/subscriptionfeature_search", subscription.SubscriptionFeatureSearch.as_view(), name="subscriptionfeature_search"),
    path("subscriptionfeature/subscriptionfeature_update/<str:subscriptionfeature_id>", subscription.SubscriptionFeatureUpdate.as_view(), name="subscriptionfeature_update"),
    path("subscriptionfeature/subscriptionfeature_delete/<str:subscriptionfeature_id>", subscription.SubscriptionFeatureDelete.as_view(), name="subscriptionfeature_delete"),
    # path("coupon/catagory_update/<str:coupon_id>", coupon.CuponUpdate.as_view(), name="coupon_update"),
    # path("coupon/coupon_delete/<str:coupon_id>", coupon.CouponDelete.as_view(), name="coupon_delete"),

    # catagory web
    path("catagory/catagory_list", catagory.CatagotyList.as_view(), name="catagory_list"),
    path("catagory/catagory_update/<str:catagory_id>", catagory.CatagotyUpdate.as_view(), name="catagory_update"),
    path("catagory/catagory_delete/<str:catagory_id>", catagory.CatagotyDelete.as_view(), name="catagory_delete"),

    # catagory api
    path("catagory/catagory_list_api", catagory.CatagotyListApi.as_view()),

    #product web
    path("product/product_list", product.AudioBookList.as_view(), name="product_list"),
    path("product/product_search", product.AudioBookSearch.as_view(), name="product_search"),
    path("product/product_filter", product.AudioBookFilter.as_view(), name="product_filter"),
    path("product/product_add", product.AudioBookAdd.as_view(), name="product_add"),
    path("product/product_update/<str:product_uid>", product.AudioBookUpdate.as_view(), name="product_update"),
    path("product/product_delete/<str:product_uid>", product.AudioBookDelete.as_view(), name="product_delete"),
    
    #product_api
    path("catagory_product_list/<str:catagory_id>", product.CatagoryProductFilter.as_view()),
    path("api_product_filter", product.ApiProductList.as_view()),
    path("api_product_detail/<str:product_uid>", product.ApiProductDetail.as_view()),

    # path("catagory/catagory_list_ajax", tests.TestAjaxList.as_view(), name="test_list_ajax"),
    # path("catagory/catagory_create", tests.TestCreate.as_view(), name="test_create"),
    # path("catagory/catagory_delete/<str:test_pk>", tests.TestDelete.as_view(), name="test_delete"),

    #credential
    path('credential/add_credential', credential.CreateCredential.as_view(), name="add_credential"),
    path('credential/change_password', credential.Change_password.as_view(), name="change_password"),
    path('credential/change_user_status', credential.UserActiveInactive.as_view(), name="change_user_status"),

    path('order/admin_order_list', order.OrderList.as_view(), name='admin_order_list'),
    path('order/admin_order_search', order.OrderSearch.as_view(), name='admin_order_search'),
    path('order/order_detail/<str:order_uid>', order.OrderDetail.as_view(), name='order_detail'),
    path('order/download_invoice/<str:order_uid>', order.DownloadInvoice.as_view(), name='download_invoice'),
    path('order/order_status_search', order.OrderStatusSearch.as_view(), name='order_status_search'),
    

    # contact message
    path("contact_messages/all_mesages/",messages.ContactMessageList.as_view(), name="all_contact_message"),
    path("contact_messages/contact_message_detail/<str:uid>",messages.ContactMessageDetail.as_view(), name="contact_message_detail"),
    path("contact_messages/contact_message_reply/<str:uid>",messages.ContactMessagereply.as_view(), name="contact_message_reply"),


]

#      admin_dashboard:download_invoice
