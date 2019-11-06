from django.shortcuts import render
from django.views.generic import ListView, DeleteView

class HomeView(ListView):
    model = item
    template_name = "home-page.html"
