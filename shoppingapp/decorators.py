from django.shortcuts import redirect
from functools import wraps

def redirect_authenticated_user(view_func):
    """
    Decorator that redirects authenticated users to the home page
    when they try to access login/register pages.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shoppingapp:home')
        return view_func(request, *args, **kwargs)
    return wrapper
