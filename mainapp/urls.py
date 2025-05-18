# urls.py

from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('mainadmin/', views.admin, name='admin'),
    path('customers/', views.all_customer_data, name='all_customer_data'),
    path('service_providers/', views.all_service_provider_data, name='all_service_provider_data'),
      path('feedbacks/', views.all_feedbacks, name='all_feedbacks'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('service_providers/add/', views.add_service_provider, name='add_service_provider'),
    path('service_providers/edit/<int:pk>/', views.edit_service_provider, name='edit_service_provider'),
    path('service_providers/delete/<int:pk>/', views.delete_service_provider, name='delete_service_provider'),
    path('feedback/delete/<int:pk>/', views.delete_feedback, name='delete_feedback'),
    path('home/', views.home, name='home'),
     path('view-messages/', views.view_messages, name='view_messages'),
     path('delete-message/<int:id>/', views.delete_message, name='delete_message'),


]

