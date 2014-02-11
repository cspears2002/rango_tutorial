from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from rango.models import Category
from rango.models import Page

def index(request):
  # context = RequestContext(request)

  category_list = Category.objects.order_by('-likes')[:5]
  context_dict = {'categories': category_list}

  return render(request, 'rango/index.html', context_dict)

def about(request):
  context_dict = {'boldmessage': 'here is the about page'}
  return render(request, 'rango/about.html', context_dict)

def category(request, category_name_url):
  category_name = category_name_url.replace('_', '')

  context_dict = {'category_name': category_name}

  try:
    category = Category.objects.get(name=category_name)

    pages = Page.objects.filter(category=category)

    context_dict['pages'] = pages
    context_dict['category'] = category
  except Category.DoesNotExist:
    pass

  return render(request, 'rango/category.html', context_dict)