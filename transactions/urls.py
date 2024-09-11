from django.urls import path
from . import views

urlpatterns = [
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('add_note/<int:pk>/', views.add_note_to_transaction, name='add_note'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_list/', views.category_list, name='category_list'),
]
