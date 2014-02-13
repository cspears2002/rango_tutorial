from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from rango.models import Category, Page

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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

  context_dict = {}
  context_dict['category_name'] = category_name
  context_dict['category_name_url'] = category_name_url

  try:
    category = Category.objects.get(name=category_name)

    pages = Page.objects.filter(category=category)

    context_dict['pages'] = pages
    context_dict['category'] = category
  except Category.DoesNotExist:
    pass

  return render(request, 'rango/category.html', context_dict)

def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)

    if form.is_valid():
      form.save(commit=True)
      return index(request)
    else:
      print form.errors
  else:
    form = CategoryForm()

  return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_url):
  category_name = remove_underscores(category_name_url)

  if request.method == 'POST':
    form = PageForm(request.POST)

    if form.is_valid():
      page = form.save(commit=False)

      try:
        cat = Category.objects.get(name=category_name)
        page.category = cat
      except Category.DoesNotExist:
        return render(request, 'rango/add_page.html', {})

      page.views = 0

      page.save()

      return category(request, category_name_url)
    else:
      print form.errors
  else:
    form = PageForm()

  return render(request, 'rango/add_page.html',
    {'category_name_url': category_name_url,
     'category_name': category_name,
     'form': form})

def register(request):
  registered = False

  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()

      user.set_password(user.password)
      user.save()

      profile = profile_form.save(commit=False)
      profile.user = user

      if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']

      profile.save()

      registered = True

    else:
      print user_form.errors, profile_form.errors

  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

  return render(request,
    'rango/register.html',
    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

