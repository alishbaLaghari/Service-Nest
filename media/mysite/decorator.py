from django.http import HttpResponseRedirect

def isLoggedIn(function):
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username', None)  # Get username from URL kwargs
        # Check if the session contains the login information
        if username is None or (username + "_login") not in request.session:
            return HttpResponseRedirect("/customer/customer_login/")  # Redirect to login page
        else:
            return function(request, *args, **kwargs)
    
    wrapper.__doc__ = function.__doc__  # Set the docstring correctly
    wrapper.__name__ = function.__name__  # Set the function name correctly
    return wrapper
