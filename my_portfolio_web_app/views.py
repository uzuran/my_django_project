"""Import render from django shortcuts"""
# views.py (in your Django app)

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
