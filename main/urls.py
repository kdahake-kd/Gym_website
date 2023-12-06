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

    
    
]