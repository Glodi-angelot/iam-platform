from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

def kibana_view(request):
    return render(request, 'monitoring/kibana.html')

def error_403_view(request):
    return render(request, 'errors/403.html', status=403)