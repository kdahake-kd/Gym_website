from django.urls import path
from main import views
app_name = 'authapp'
urlpatterns = [
    path('',views.Home,name="Home"),
    path('signup',views.signup,name="signup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handleLogout,name="handleLogout"),
    path('join',views.enroll,name="enroll"),
    path('profile',views.profile,name="profile"),
    path('contact',views.contact,name="contact"),
    path('gallery',views.gallery,name="gallery"),
    path('attendance',views.attendance,name="attendance"),
     path('services',views.services,name="services"),
    path('blog',views.post_list,name='blog'),
    path('shop',views.shop,name='shop'),
    path('about',views.about,name='about'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('fetch_data',views.fetch_data,name="fetch_data")

    
    
]