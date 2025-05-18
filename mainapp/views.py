from django.shortcuts import render, get_object_or_404, redirect
from customer.models import CustomerDetails, CustomerLogin,Feedback
from service_provider.models import ServiceProviderDetails, ServiceProviderLogin
from django.contrib import messages
from .models import message
from django.contrib.auth.hashers import make_password

# View to render admin panel
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        # Create and save a new Message instance
        if name and email and message_text:  # Basic validation
            message.objects.create(name=name, email=email, message=message_text)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')  # Redirect to the home page or another page
        else:
            messages.error(request, 'Please fill out all fields.')
    
    return render(request, 'home.html')
def admin(request):
    customer_count = CustomerDetails.objects.count()
    provider_count = ServiceProviderDetails.objects.count()
    feedback_count = Feedback.objects.count()
    message_count=message.objects.count()

    context = {
        'customer_count': customer_count,
        'provider_count': provider_count,
        'feedback_count': feedback_count,
        'message_count':message_count,
    }
    return render(request, 'admin.html', context)

def view_messages(request):
    messages = message.objects.all()
    return render(request, 'messages.html', {'messages': messages})


def delete_message(request, id):
    if request.method == 'POST':
        text_message = get_object_or_404(message, id=id)
        text_message.delete()
    return redirect('view_messages')

from django.db.models import Count
def all_feedbacks(request):
    customers_with_feedback = CustomerDetails.objects.annotate(
        feedback_count=Count('feedback')
    ).filter(feedback_count__gt=0)

    feedbacks = Feedback.objects.all()
    
    context = {
        'customer_signup_details': customers_with_feedback,
        'feedbacks': feedbacks,
    }
    return render(request, 'feedbacks.html', context)
def delete_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully!')
        return redirect('all_feedbacks')  # Ensure the redirect URL name matches the view name
    return render(request, 'feedbacks.html', {'feedback': feedback})

# View to display all customer data
def all_customer_data(request):
    customer_signup_details = CustomerDetails.objects.all()
    customer_login_details = CustomerLogin.objects.all()

    context = {
        'customer_signup_details': customer_signup_details,
        'customer_login_details': customer_login_details,
    }
    return render(request, 'customers.html', context)

# View to display all service provider data
def all_service_provider_data(request):
    service_provider_signup_details = ServiceProviderDetails.objects.all()
    service_provider_login_details = ServiceProviderLogin.objects.all()

    context = {
        'service_provider_signup_details': service_provider_signup_details,
        'service_provider_login_details': service_provider_login_details,
    }
    return render(request, 'service_providers.html', context)

# View to add a new customer
def add_customer(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        city = request.POST.get('city')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomerLogin.objects.filter(username=username).exists() or CustomerDetails.objects.filter(email=email).exists():
            error_message = 'Username or email already exists. Please choose a different one.'
            return render(request, 'add_customer.html', {'error': error_message})

        customer_details = CustomerDetails.objects.create(
            full_name=full_name,
            age=age,
            city=city,
            email=email
        )

        # Hash the password before saving
        hashed_password = make_password(password)
        CustomerLogin.objects.create(
            customer_details=customer_details,
            username=username,
            password=hashed_password
        )

        return redirect('add_customer')
    else:
        return render(request, 'add_customer.html')

# View to edit a customer's details
# views.py - edit_customer view


def edit_customer(request, customer_id):
    customer = get_object_or_404(CustomerDetails, id=customer_id)
    customer_login = customer.customerlogin  # Adjust this based on your actual field name in CustomerDetails
    
    if request.method == 'POST':
        # Retrieve updated values from the POST request
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        city = request.POST.get('city')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Update the customer details
        customer.full_name = full_name
        customer.age = age
        customer.city = city
        customer.email = email
        
        # Update CustomerLogin details
        customer_login.username = username
        
        # Hash the new password before saving
        if password:
            customer_login.password = make_password(password)
        
        # Handle profile photo upload
        if 'profile_photo' in request.FILES:
            customer.profile_photo = request.FILES['profile_photo']
        
        # Save changes
        customer.save()
        customer_login.save()
        
        # Redirect to customers.html after successful update
        return redirect('all_customer_data')  # Adjust this URL name as per your URL configuration

    # Render the edit form with the current customer details
    context = {
        'customer': customer,
        'customer_login': customer_login,
    }
    return render(request, 'edit_customer.html', context)

# View to delete a customer
def delete_customer(request, pk):
    customer = get_object_or_404(CustomerDetails, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('all_customer_data')
    return render(request, 'delete_customer.html', {'customer': customer})

# View to add a new service provider


def add_service_provider(request):
    if request.method == 'POST':
        # Handle form submission
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        service_types = request.POST.getlist('service_types')
        previous_work_experience = request.POST.get('previous_work_experience')
        working_hours = request.POST.get('working_hours')
        days_available = request.POST.get('days_available')
        languages = request.POST.get('languages')
        skills_and_qualifications = request.POST.get('skills_and_qualifications')
        description = request.POST.get('description')
        city = request.POST.get('city')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if username or email already exists
        if ServiceProviderLogin.objects.filter(username=username).exists():
            error_message = 'Username already exists. Please choose a different one.'
            return render(request, 'add_service_provider.html', {'error': error_message})
        
        if ServiceProviderDetails.objects.filter(email=email).exists():
            error_message = 'Email already exists. Please choose a different one.'
            return render(request, 'add_service_provider.html', {'error': error_message})

        # Hash the password
        hashed_password = make_password(password)

        # Save to database
        provider_details = ServiceProviderDetails.objects.create(
            full_name=full_name,
            dob=dob,
            gender=gender,
            phone=phone,
            email=email,
            city=city,
            address=address,
            service_types=', '.join(service_types),  # Store as comma-separated string
            previous_work_experience=previous_work_experience,
            working_hours=working_hours,
            days_available=days_available,
            languages=languages,
            skills_and_qualifications=skills_and_qualifications,
            description=description,
        )

        # Create SignIn record
        ServiceProviderLogin.objects.create(
            username=username,
            password=hashed_password,
            service_provider_details=provider_details
        )

        # Redirect to the login success page with the correct URL pattern and name
        return redirect('add_service_provider')
    
    else:
        return render(request, 'add_service_provider.html')
# View to edit a service provider's details

def edit_service_provider(request, pk):
    provider = get_object_or_404(ServiceProviderDetails, pk=pk)
    provider_login = provider.serviceproviderlogin  # Adjust based on your actual related name

    if request.method == 'POST':
        # Update fields from request.POST directly
        provider.full_name = request.POST.get('full_name')
        provider.dob = request.POST.get('dob')
        provider.gender = request.POST.get('gender')
        provider.phone = request.POST.get('phone')
        provider.email = request.POST.get('email')
        provider.city = request.POST.get('city')
        provider.address = request.POST.get('address')
        
        # Correctly handle service types - use the string field
        provider.service_types = request.POST.get('service_types_str', '')
        
        provider.previous_work_experience = request.POST.get('previous_work_experience')
        provider.working_hours = request.POST.get('working_hours')
        provider.days_available = request.POST.get('days_available')
        provider.languages = request.POST.get('languages')
        provider.skills_and_qualifications = request.POST.get('skills_and_qualifications')
        provider.description = request.POST.get('description')
        
        # Handle profile photo upload
        if 'profile_photo' in request.FILES:
            provider.profile_photo = request.FILES['profile_photo']
        
        # Update ServiceProviderLogin details
        provider_login.username = request.POST.get('username')
        new_password = request.POST.get('password')
        
        # Hash the new password before saving
        if new_password:
            provider_login.password = make_password(new_password)
        
        # Save changes
        provider.save()
        provider_login.save()
        
        messages.success(request, 'Service provider updated successfully!')
        return redirect('all_service_provider_data')
    
    return render(request, 'edit_service_provider.html', {'provider': provider, 'provider_login': provider_login})


def delete_service_provider(request, pk):
    provider = get_object_or_404(ServiceProviderDetails, pk=pk)
    if request.method == 'POST':
        provider.delete()
        messages.success(request, 'Service provider deleted successfully!')
        return redirect('all_service_provider_data')
    return render(request, 'delete_service_provider.html', {'provider': provider})
