from django.db import models
from service_provider.models import ServiceProviderDetails 

class CustomerDetails(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    accepted = models.BooleanField(default=False)

class CustomerLogin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    customer_details = models.OneToOneField(CustomerDetails, on_delete=models.CASCADE)

class Request(models.Model):
    request = models.BooleanField(default=False)
    accept = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    customer_details = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    service_provider_details = models.ForeignKey(ServiceProviderDetails, on_delete=models.CASCADE)
    
    # New fields for service request details
    service_type = models.CharField(max_length=100, blank=True, null=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=50, blank=True, null=True)
    service_location = models.CharField(max_length=100, blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    additional_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @classmethod
    def create_request(cls, customer_details, provider_details, **kwargs):
        request_data = {
            'customer_details': customer_details,
            'service_provider_details': provider_details,
            'request': True
        }
        
        # Add any additional fields from kwargs
        for field in ['service_type', 'preferred_date', 'preferred_time', 
                      'service_location', 'service_description', 'additional_requirements']:
            if field in kwargs:
                request_data[field] = kwargs[field]
                
        return cls.objects.create(**request_data)
    
    def __str__(self):
        service_info = f" ({self.service_type})" if self.service_type else ""
        return f"Request from {self.customer_details.full_name} to {self.service_provider_details.full_name}{service_info}"


class Feedback(models.Model):
    customer_details = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    service_provider_details = models.ForeignKey(ServiceProviderDetails, on_delete=models.CASCADE)
    feedback = models.TextField()
    request = models.ForeignKey(Request, on_delete=models.CASCADE)