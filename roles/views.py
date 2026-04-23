from django.shortcuts import render

def roles_page(request):
    return render(request, 'roles/roles.html')