from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
	return render(request, 'userd/index.html')

def signin(request):
	return render(request, 'userd/signin.html')

def register(request):
	return render(request, 'userd/register.html')

def reg(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if 'id' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			if 'reg' in request.POST:
				return redirect('/adduser')
			else:
				return redirect('/register')
		else:
			if 'reg' in request.POST:
				return redirect('/dashboard')
			else:
				request.session['id'] = errors['id']
				request.session['user_level'] = errors['user_level']
				return redirect('/dashboard')
	return redirect('/register')

def login(request):
	if request.method == "POST":
		errors = User.objects.login_validator(request.POST)
		if 'id' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/signin')
		else:
			request.session['id'] = errors['id']
			request.session['user_level'] = errors['user_level']
			if request.session['user_level'] == "admin":
				return redirect('/dashboard')
			else:
				return redirect('/dashboard')
	return redirect('/signin')

def dashboard(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		context = {
				'users': User.objects.all()
			}
		if request.session['user_level'] == "normal":
			return render(request, 'userd/userdash.html', context)
		else:
			return render(request, 'userd/admindash.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')

def edit(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		context = {
				'user': User.objects.get(id = request.session['id'])
			}
		return render(request, 'userd/edit.html', context)

def editinfo(request):
	if request.method == "POST":
		errors = User.objects.editinfo_validator(request.POST)
		if 'success' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			if request.session['user_level'] == 'admin':
				return redirect('/users/edit/' + str(request.POST['uid']))
			else: 
				return redirect('/users/edit')
		else:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			if request.session['user_level'] == 'admin':
				return redirect('/users/edit/' + str(request.POST['uid']))
			else: 
				return redirect('/users/edit')
	else:
		return redirect('/users/edit')

def editpword(request):
	if request.method == "POST":
		errors = User.objects.editpword_validator(request.POST)
		if 'success' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			if request.session['user_level'] == 'admin':
				return redirect('/users/edit/' + str(request.POST['uid']))
			else: 
				return redirect('/users/edit')
		else:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			if request.session['user_level'] == 'admin':
				return redirect('/users/edit/' + str(request.POST['uid']))
			else: 
				return redirect('/users/edit')
	else:
		return redirect('/users/edit')

def editdesc(request):
	if request.method == "POST":
		errors = User.objects.editdesc_validator(request.POST)
		if 'success' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/users/edit')
		else:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/users/edit')
	else:
		return redirect('/users/edit')

def edituser(request, uid):
	if 'id' not in request.session or request.session['user_level'] == 'admin':
		context = {
			'user': User.objects.get(id = uid)
		}
		return render(request, 'userd/edituser.html', context)
	else:
		if 'id' not in request.session:
			return redirect('/')
		else:
			return redirect('/dashboard')

def adduser(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		if request.session['user_level'] == 'admin':
			return render(request, 'userd/adduser.html')
		else:
			return redirect('/dashboard')

def remove(request, uid):
	if 'id' not in request.session:
		return redirect('/')
	else:
		if request.session['user_level'] == 'admin':
			context = {'id': uid}
			return render(request, 'userd/remove.html', context)
		else:
			return redirect('/dashboard')

def removeuser(request):
	if request.method == "POST":
		User.objects.delete(request.POST['uid'])
		return redirect('/dashboard')
	else:
		return redirect('/dashboard')

def showuser(request, uid):
	if 'id' not in request.session:
		return redirect('/')
	else:
		message = Message.objects.filter(receiver_id = uid)
		comments = Comment.objects.all()
		context = {
			'user': User.objects.get(id = uid),
			'msg' : message,
			'cmnt' : comments
		}
		return render(request, 'userd/showuser.html', context)

def pstmsg(request):
	if request.method == "POST":
		errors = User.objects.msgvalid(request.POST)
		if 'success' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
				return redirect('/users/show/' + str(request.POST['rid']))
		else:
			return redirect('/users/show/' + str(request.POST['rid']))
	else:
		return redirect('/users/show/' + str(request.POST['rid']))

def pstcmnt(request):
	if request.method == "POST":
		errors = User.objects.cmntvalid(request.POST)
		if 'success' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
				return redirect('/users/show/' + str(request.POST['rid']))
		else:
			return redirect('/users/show/' + str(request.POST['rid']))
	else:
		return redirect('/users/show/' + str(request.POST['rid']))

