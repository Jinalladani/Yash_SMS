from django.urls import path, include
from django.contrib.auth import views as auth_views

from authentication import views


urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]