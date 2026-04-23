from django.shortcuts import render

def users_page(request):
    return render(request, 'users_app/users.html')