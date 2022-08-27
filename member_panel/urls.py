from django.urls import path
from member_panel import views

urlpatterns = [
    path('', views.SocietyListView.as_view(), name='member-society-list'),
    path('member-login/', views.MemberLoginView.as_view(), name='member-login'),
    path('member-logout/', views.MemberLogoutView.as_view(), name='member-logout'),
    path('member-otp-verification/', views.MemberOtpVerification.as_view(), name='member-otp-verification'),
    path('member-dashboard/<int:pk>', views.MemberDashboard.as_view(), name='member-dashboard'),
    path("member-dashboard-detail/<slug:detail_type>", views.MemberDashboardDetailView.as_view(), name="member-dashboard-detail"),
    path('member-income-expense-ledger/<int:pk>', views.MemberIncomeExpenseLedger.as_view(), name='member-income-expense-ledger'),
]
