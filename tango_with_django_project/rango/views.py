from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from rango.models import Category

def index(request):
  # context = RequestContext(request)

  category_list = Category.objects.order_by('-likes')[:5]
  context_dict = {'categories': category_list}

  return render(request, 'rango/index.html', context_dict)

def about(request):
  context_dict = {'boldmessage': 'here is the about page'}
  return render(request, 'rango/about.html', context_dict)