from django.shortcuts import redirect


def doctor_only(view_func):

    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'doctors':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')

    return wrapper_function


def not_auth_doctor(view_func):

    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'doctors':
            return redirect('doctor_home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_function
