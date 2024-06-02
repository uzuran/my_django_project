"""Import render from django shortcuts"""
# views.py (in your Django app)

from django.shortcuts import render


def index(request):
    """Return render index.html"""
    return render(request, 'index.html')
