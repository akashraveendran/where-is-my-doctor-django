from django.shortcuts import redirect


def admin_only(view_func):

    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                return redirect('index')
        else:
            return redirect('index')

    return wrapper_function