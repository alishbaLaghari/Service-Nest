from django.urls import path
from customer import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mysite.decorator import isLoggedIn


urlpatterns = [
    path('customer_signup/', views.signup, name='customer_signup'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('customer_login_success/<str:username>/', isLoggedIn(views.customer_login_success), name='customer_login_success'),
    path('profile/<str:username>/', isLoggedIn(views.profile), name='customer_profile'),
   path('provider_details/<int:pk>/<str:username>/', views.provider_details, name='provider_details'),
    path('pending/<int:pk>/', (views.pending), name='pending'),
    path('pending-requests/', (views.pending_requests), name='pending_requests'),
    path('cancel-request/<int:pk>/', (views.cancel_request), name='cancel_request'),
    path('submit_feedback/', (views.submit_feedback), name='submit_feedback'),
    path('complete_request/<int:req_id>/', (views.complete_request), name='complete_request'),
    path('load-chat/', views.load_chat, name='load_chat'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

