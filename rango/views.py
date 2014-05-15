from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from rango.models import Category, Page
from rango.form import CategoryForm, PageForm, UserForm, UserProfileForm

# Create your views here.
def index(request):
	category_list = Category.objects.order_by('-name')[:5]
	context_dict = {'categories': category_list}
	for category in category_list:
		category.url = category.name.replace(' ', '_')

	return render(request, 'rango/index.html', context_dict)

def about(request):
	return HttpResponse("About page")

def category(request, category_name_url):
	category_name = category_name_url.replace('_', ' ')
	context_dict = {'category_name' : category_name, 'category_name_url' : category_name_url}

	try:
		category = Category.objects.get(name = category_name)

		pages = Page.objects.filter(category = category)

		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)

def add_category(request):
	#context = RequestContext(request)

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form' : form})

def add_page(request, category_name_url):
	#context = RequestContext(request)
	category_name = category_name_url.replace('_', ' ')

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit = False)

			try:
				cat = Category.objects.get(name = category_name)
				page.category = cat
			except Category.DoesNotExist:
				return render(request, 'rango/add_category.html')

			page.views = 0
			page.save()

			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()

	return render(request, 'rango/add_page.html', {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form})

def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
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
	return render(request, 'rango/register.html', {'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

		if user:
			if user.is_active:
				login(request, user)
				#return render(request, 'rango/index.html', {'username' : user.username})
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
	else:
		return render(request, 'rango/login.html', {})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')
