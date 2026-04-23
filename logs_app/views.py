from django.shortcuts import render

def logs_page(request):
    return render(request, 'logs_app/logs.html')
