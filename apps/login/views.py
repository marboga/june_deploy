from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
	users = User.objects.all()
	context = {
		'users': users
	}
	return render(request, 'login/index.html', context)

def register(request):
	if request.method == 'POST':
		response = User.objects.validate_registration(request.POST)
		if response[0] == True:
			print response[1]
			print response[1].first_name
			request.session['first_name'] = response[1].first_name
			request.session['id'] = response[1].id
			return redirect('review_app:index')
		else:
			for err in response[1]:
				messages.error(request, err)
	return redirect('auth:index')

def login(request):
	if request.method == "GET":
		messages.warning(request, 'error')
		return redirect('auth:index')
	else:
		(valid, data) = User.objects.validate_login(request.POST)
		if valid:
			request.session['id'] = data.id
			return redirect('review_app:index')
		else:
			for error in data:
				messages.warning(request, error)
		return redirect('auth:index')

def logout(request):
	request.session.clear()
	return redirect('login:index')