from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('add_note/<int:pk>/', views.add_note_to_transaction, name='add_note'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_list/', views.category_list, name='category_list'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('stats/', views.stats_view, name='stats'),
    path('category_pie_chart/', views.category_pie_chart, name='category_pie_chart'),
    path('compare_periods/', views.compare_periods, name='compare_periods'),
    path('income_pie_chart/', views.income_pie_chart, name='income_pie_chart'),

]
