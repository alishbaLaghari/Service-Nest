from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import CustomerDetails, CustomerLogin, Request, Feedback
from service_provider.models import ServiceProviderDetails
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
from django.templatetags.static import static

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        city = request.POST.get('city')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomerLogin.objects.filter(username=username).exists() or CustomerDetails.objects.filter(email=email).exists():
            error_message = 'Username or email already exists. Please choose a different one.'
            return render(request, 'customer_signup.html', {'error': error_message})

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

        return redirect('customer_login')
    else:
        return render(request, 'customer_signup.html')

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        customer_login = CustomerLogin.objects.filter(username=username).first()
        if customer_login and check_password(password, customer_login.password):
            request.session[username + "_login"] = True  # Store in session to track login
            return redirect('customer_login_success', username=username)
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'customer_login.html', {'error': error_message})
    else:
        return render(request, 'customer_login.html')

def customer_login_success(request, username):
    customer_login = get_object_or_404(CustomerLogin, username=username)
    customer_details = customer_login.customer_details

    service_providers = ServiceProviderDetails.objects.all()
    location_filter = request.GET.get('location', customer_details.city)
    category_filter = request.GET.getlist('categories')

    if location_filter and location_filter != "All":
        service_providers = service_providers.filter(city=location_filter)

    if category_filter:
        for category in category_filter:
            service_providers = service_providers.filter(service_types__icontains=category.strip())

    # Get pending request count for badge display
    pending_count = Request.objects.filter(
        customer_details=customer_details,
        request=True,
        completed=False
    ).count()

    context = {
        'username': username,
        'customer_details': customer_details,
        'service_providers': service_providers,
        'locations': ['Karachi', 'Lahore', 'Islamabad', 'Hyderabad', 'Jamshoro','sialkot','All'],
        'categories': ['Mechanic', 'Chef', 'Barber', 'Housekeeper', 'Plumber', 'Electrician', 'Gardener', 'Painter', 'Carpenter', 'Mover', 'Catering', 'Handyman', 'Janitor','tutor'],
        'customer_city': customer_details.city,
        'pending_count': pending_count,
    }
    return render(request, 'customer_login_success.html', context)

def profile(request, username):
    customer_login = get_object_or_404(CustomerLogin, username=username)
    customer_details = customer_login.customer_details

    if request.method == 'POST':
        if 'profile_photo' in request.FILES:
            profile_photo = request.FILES['profile_photo']
            customer_details.profile_photo = profile_photo

        customer_details.full_name = request.POST.get('full_name', customer_details.full_name)
        customer_details.age = request.POST.get('age', customer_details.age)
        customer_details.city = request.POST.get('city', customer_details.city)
        
        customer_details.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('customer_profile', username=username)

    return render(request, 'customer_profile.html', {'customer_details': customer_details, 'username': username})

def provider_details(request, pk, username):
    provider = get_object_or_404(ServiceProviderDetails, pk=pk)
    customer_details = get_object_or_404(CustomerDetails, customerlogin__username=username)
    feedbacks = Feedback.objects.filter(service_provider_details=provider)
    
    # Check if a request already exists
    existing_request = Request.objects.filter(
        customer_details=customer_details,
        service_provider_details=provider,
        request=True
    ).exists()
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        confirm_request = request.POST.get('confirm_request')
        
        if confirm_request == 'true':  # From the form submission
            # Get form data
            service_type = request.POST.get('service_type')
            preferred_date = request.POST.get('preferred_date')
            preferred_time = request.POST.get('preferred_time')
            service_location = request.POST.get('service_location')
            service_description = request.POST.get('service_description')
            additional_requirements = request.POST.get('additional_requirements')
            
            # Create request with all the data
            Request.create_request(
                customer_details=customer_details,
                provider_details=provider,
                service_type=service_type,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                service_location=service_location,
                service_description=service_description,
                additional_requirements=additional_requirements
            )
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            # If it's a regular form submission
            messages.success(request, 'Your service request has been sent successfully!')
            return redirect('provider_details', pk=pk, username=username)
        else:
            # Handle regular submission (non-form)
            customer_details = get_object_or_404(CustomerDetails, id=customer_id)
            Request.create_request(customer_details=customer_details, provider_details=provider)
            return redirect('provider_details', pk=pk, username=username)
    
    context = {
        'provider': provider,
        'username': username,
        'customer_details': customer_details,
        'feedbacks': feedbacks,
        'existing_request': existing_request,
        'today_date': date.today()  # For the date picker min attribute
    }
    
    return render(request, 'provider_details.html', context)

def pending_requests(request):
    if hasattr(request.user, 'customer'):
        pending_requests = Request.objects.filter(customer=request.user.customer)
        requests = CustomerDetails.objects.filter(customer=request.user)
        context = {
        'requests': requests,
    }

        return render(request, 'pending.html', {'requests': pending_requests},context)
    else:
        messages.error(request, 'Customer details not found.')
        return render(request, 'pending.html')

def cancel_request(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(Request, pk=pk)
        req.delete()
        messages.success(request, 'Request canceled successfully.')
        customer_pk = req.customer_details.pk
        return redirect('pending', pk=customer_pk)

    return redirect('pending')

def pending(request, pk):
    customer = get_object_or_404(CustomerDetails, pk=pk)
    requests = Request.objects.filter(customer_details=customer, request=True)
    return render(request, 'pending.html', {'requests': requests, 'customer': customer})

def submit_feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        request_id = request.POST.get('request_id')
        customer_id = request.POST.get('customer_id')
        service_provider_id = request.POST.get('service_provider_id')

        request_obj = get_object_or_404(Request, pk=request_id, customer_details_id=customer_id, service_provider_details_id=service_provider_id)

        feedback = Feedback.objects.create(
            customer_details_id=customer_id,
            service_provider_details_id=service_provider_id,
            request=request_obj,
            feedback=feedback_text
        )

        return JsonResponse({'success': True})

        return redirect('pending_requests')  # Redirect to the pending requests page

def complete_request(request, req_id):
    request_obj = get_object_or_404(Request, pk=req_id)
    if request.method == 'POST':
        request_obj.completed = True
        request_obj.save()
        return redirect('pending', pk=request_obj.customer_details.pk)
    return redirect('pending')

def pending_requests(request):
    pending_requests = Request.objects.filter(completed=False)
    completed_requests = Request.objects.filter(completed=True)
    context = {
        'requests': pending_requests,
        'completed_requests': completed_requests,
    }
    return render(request, 'pending.html', context)

def load_chat(request):
    """Load the chat interface as a partial template."""
    provider_id = request.GET.get('provider_id')
    customer_id = request.GET.get('customer_id')
    
    context = {}
    
    if provider_id:
        # Customer is chatting with a provider
        provider = get_object_or_404(ServiceProviderDetails, id=provider_id)
        context['receiver_name'] = provider.full_name
        context['receiver_profile_pic'] = provider.profile_photo.url if provider.profile_photo else static('default.png')
    
    elif customer_id:
        # Provider is chatting with a customer
        customer = get_object_or_404(CustomerDetails, id=customer_id)
        context['receiver_name'] = customer.full_name
        context['receiver_profile_pic'] = customer.profile_photo.url if customer.profile_photo else static('default.png')
    
    return render(request, 'components/chat_interface.html', context)

