"""Simple template-based views."""

from django.views.generic import TemplateView

class HomeView(TemplateView):
    # Renders templates/pages/home.html
    template_name = "pages/home.html"
