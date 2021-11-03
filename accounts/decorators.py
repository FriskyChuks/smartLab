from django.http import HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return view_func(request, *args, **kwargs)
            

    return wrapper_func


def allowed_users(alllowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            user_group = None
            if request.user.group:
                user_group = request.user.group.name

            if user_group in alllowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, "Unauthorized page! thanks.")
                return HttpResponseRedirect('/accounts/logout')
        return wrapper_func
    return decorator 