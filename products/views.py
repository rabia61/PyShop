from django.http import HttpResponse
from django.shortcuts import render
from .models import Product


def index(request):
    products = Product.objects.all()
    return render(request, 'reports.html', {'products': products})


def first_product(request):
    return HttpResponse('First response')