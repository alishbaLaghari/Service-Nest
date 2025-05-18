from django.http import HttpResponseRedirect

def isLoggedIn(view_func):
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username', None)  # Get username from URL kwargs
        print(f"Decorator: Checking if {username} is logged in.")  # Debug print
        # Check if the session contains the login information
        if username is None or (username + "_login") not in request.session:
            print(f"Decorator: {username} is not logged in. Redirecting to login page.")  # Debug print
            return HttpResponseRedirect("/service/login/")  # Redirect to login page
        else:
            print(f"Decorator: {username} is logged in. Proceeding to view.")  # Debug print
            return view_func(request, *args, **kwargs)
    
    wrapper.__doc__ = view_func.__doc__  # Set the docstring correctly
    wrapper.__name__ = view_func.__name__  # Set the function name correctly
    return wrapper
