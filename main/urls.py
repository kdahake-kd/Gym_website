from django.urls import path
from main import views
app_name = 'authapp'
urlpatterns = [
    path('',views.Home,name="Home"),
    
    
]