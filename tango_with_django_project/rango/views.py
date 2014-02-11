from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm

def remove_spaces(category_list):
  for category in category_list:
    category.url = category.name.replace(' ', '_')
  return category_list

def remove_underscores(category_name_url):
  category_name = category_name_url.replace('_', ' ')
  return category_name

def index(request):
  context_dict = {}

  category_list = Category.objects.order_by('-likes')[:5]
  category_list = remove_spaces(category_list)
  context_dict['categories'] = category_list

  page_list = Page.objects.order_by('-views')[:5]
  context_dict['pages'] = page_list

  return render(request, 'rango/index.html', context_dict)

def about(request):
  context_dict = {'boldmessage': 'here is the about page'}
  return render(request, 'rango/about.html', context_dict)

def category(request, category_name_url):
  category_name = remove_underscores(category_name_url)

  context_dict = {'category_name': category_name}

  try:
    category = Category.objects.get(name=category_name)

    pages = Page.objects.filter(category=category)

    context_dict['pages'] = pages
    context_dict['category'] = category
  except Category.DoesNotExist:
    pass

  return render(request, 'rango/category.html', context_dict)

def add_category(request):
  if request.method = 'POST':
    form = CategoryForm(request.POST)

    if form.is_valid():
      form.save(commit=True)
      return index(request)
    else:
      print form.errors
  else:
    form = CategoryForm()

  return render(request, 'rango/add_category.html', {'form': form})