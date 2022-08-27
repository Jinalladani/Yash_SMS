from django.urls import path, include
from django.contrib.auth import views as auth_views

from authentication import views


urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "authentication/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "authentication/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "authentication/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "authentication/password_reset_done.html"), name ='password_reset_complete')
]