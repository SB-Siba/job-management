from django.urls import path
from . import views

from . import authentication
from .checkout import checkout
from .manage_address import address
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

    #checkout cart
    # path("api/get_cart_list", checkout.CartList.as_view()),
    # path("api/add_to_cart/<str:product_uid>", checkout.ApiAddTOCart.as_view()),
    # path("api/cart_update_delete/<str:product_uid>", checkout.ApiCartUpdateDelete.as_view()),
    # path("api/apply_coupon/<str:coupon_code>", checkout.ApplyCoupon.as_view()),
    # path("api/remove_coupon/<str:coupon_code>", checkout.ApplyCoupon.as_view()),

    # place order
    # path("api/place_order", checkout.PlaceOrder.as_view()),
    path("api/order_list", checkout.OrderList.as_view()),
    path("api/order_detail/<str:uid>", checkout.OrderDetail.as_view()),
    # path("api/order_cancel_return_refund/<str:order_uid>", checkout.OrderCancelReturnRefund.as_view()),

    #address
    # path("api/manage_address", address.AddressManage.as_view()),

    # #contact message
    # path('api/contact_message_filter', contact.AllMessageListApi.as_view()),
    # path('api/create/contact_message', contact.MessageCreateApi.as_view()),

]

#    app_common:privacy_policy