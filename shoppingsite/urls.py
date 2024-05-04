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

app_name = 'shoppingsite'

urlpatterns = [
    #Authentication urls
    path('login', authenticate.Login.as_view(), name = "login"),
    path('signup', authenticate.Registration.as_view(), name = "signup"),
    path("passwordChange/",auth_view.PasswordChangeView.as_view(template_name = 'shoppingsite/authtemp/changepassword.html',form_class = PasswordChangeForm,success_url = '/passwordchangedone'),name='passwordchange'),
    path("passwordchangedone/",auth_view.PasswordChangeDoneView.as_view(template_name = 'shoppingsite/authtemp/changepassworddone.html'),name='passwordchangedone'),
    path('password-reset/', PasswordResetView.as_view(template_name='shoppingsite/authtemp/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='shoppingsite/authtemp/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='shoppingsite/authtemp/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='shoppingsite/authtemp/password_reset_complete.html'),name='password_reset_complete'),
    path('logout', authenticate.Logout.as_view(), name = "logout"),
    
    #Page Urls
    path('',views.HomeView.as_view(),name="home"),
    path('profile',views.ProfileView.as_view(),name="profile"),
    path('alladdress',views.AllAddress.as_view(),name="alladdress"),
    path('addaddress',views.AddAddress.as_view(),name="addaddress"),
    path('delete-address/<str:address_id>/', views.DeleteAddress.as_view(), name='delete_address'),
    path('updateprofile',views.UpdateProfileView.as_view(),name="updateprofile"),
    path('productsofcategory/<str:c_name>',views.showProductsViews.as_view(),name="productsofcategory"),
    path('productdetails/<int:p_id>',views.ProductDetailsView.as_view(),name="productdetails"),
    path('showcart',views.ShowCart.as_view(),name='showcart'),
    path('addtocart',views.AddToCartView.as_view(),name='addtocart'),
    path("manage-cart/<int:product_uid>/", views.ManageCart.as_view(), name="managecart"),
    path('removefromcart/<int:cart_id>/remove/<str:rp_name>',views.RemoveFromCart,name='removefromcart'),
    # path('checkout/',views.Checkout.as_view(),name='checkout'),
    # path('paymenthandler/',views.PaymentHandler.as_view(),name='paymenthandler'),
    path('paymentsuccess/<int:cart_id>',views.PaymentSuccess.as_view(),name='paymentsuccess'),
    # path('directbuychecout/<int:p_id>',views.DirectBuyCheckout.as_view(),name='directbuychecout'),
    path('directbuy/<int:p_uid>',views.DirectBuy.as_view(),name='directbuy'),
    path('pricingpage',views.PricingPageView.as_view(),name='pricing'),
    path('subscriptioncheckout/<int:plan_id>',views.SubscriptionChecout.as_view(),name='subscriptioncheckout'),
    path('usertakesubscription/<int:plan_id>',views.UserTakeSubscription,name='usertakesubscription'),
    path('invoice/<int:order_uid>',views.UserDownloadInvoice.as_view(),name="invoice"),
    path('subscriptionaudiobooks',views.SubscriptionAudioBooks.as_view(),name='subscriptionaudiobooks'),
    path('subscribebookepisodes/<int:book_id>',views.SubscribeBooksEpisode.as_view(),name='subscribebookepisodes'),
    path('removeaudio',views.remove_audio,name='remove-audio'),

    path('orders',views.OrderView.as_view(),name='orders'),
]