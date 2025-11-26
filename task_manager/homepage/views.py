from django.shortcuts import render


def index(request):
    a = None
    a.hello()
    return render(request, 'homepage/index.html', {})
