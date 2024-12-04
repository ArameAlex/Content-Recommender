from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import ContentModel, ViewCountModel


# class HomeView(TemplateView):
#     template_name = "ContentApp/home.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["content"] = ContentModel.objects.all()
#         return context

def home(request):
    data = ContentModel.objects.all()
    context = {"contents": data}
    return render(request, "ContentApp/home.html", context)
