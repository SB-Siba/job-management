from django.urls import path
from . import views,authenticate

app_name = 'shoppingsite'

urlpatterns = [
    path('login', authenticate.Login.as_view(), name = "login"),
    path('signup', authenticate.Registration.as_view(), name = "signup"),
    path('logout', authenticate.Logout.as_view(), name = "logout"),
    path('',views.HomeView.as_view(),name="home"),
    path('profile',views.ProfileView.as_view(),name="profile"),
    path('updateprofile',views.UpdateProfileView.as_view(),name="updateprofile"),
    path('productsofcategory/<str:c_name>',views.showProductsViews.as_view(),name="productsofcategory"),
    path('productdetails/<int:p_id>',views.ProductDetailsView.as_view(),name="productdetails"),
    path('play/<int:audio_id>/', views.play_audio_demo, name='play_audio_demo'),
    path('playepisodes/<int:audio_id>/', views.play_audio_episodes, name='play_audio_episodes'),
    path('showcart',views.ShowCart.as_view(),name='showcart'),
    path('addtocart',views.AddToCart.as_view(),name='addtocart'),
    path('removefromcart/<int:rp_id>',views.RemoveFromCart,name='removefromcart'),
    path('subscriptionaudiobooks',views.SubscriptionAudioBooks.as_view(),name='subscriptionaudiobooks'),
    path('subscribebookepisodes/<int:book_id>',views.SubscribeBooksEpisode.as_view(),name='subscribebookepisodes'),

]