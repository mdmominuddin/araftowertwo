from django.urls import path
from . import views
from .views import ReportView

urlpatterns = [
    path('', views.public_home, name='home'),
    path('homepage/', views.home, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('deposit/', views.create_deposit, name='deposit'),
    path('expense/', views.create_expense, name='expense'),
    path('monthly-summary/', views.monthly_summary, name='monthly_summary'),
    path('category-wise-summary/', views.category_wise_summary, name='category_wise_summary'),
    path('expense-detail/', views.DetailExpens, name='expense_detail'),
    path('deposit-detail/', views.DepositDetails, name='deposit_detail'),
    path('members/', views.Member, name='member_list'),
    path('report/', ReportView.as_view(), name='report'),  # Updated for ReportView
    path('individual_contributions/<int:member_id>/', ReportView.as_view(), name='individual_contributions'),  # Added for individual contributions
    # Add other URLs for your app as needed
]

