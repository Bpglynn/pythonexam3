from django.shortcuts import render, redirect, HttpResponse
from apps.users.models import validation, database, users
from django import forms
from django.contrib import messages

# Create your views here.

# The success function is the breakout point to other apps if a user successfully creates an account or logs on. 

def index(request):
	print("index: Get request")
	return render(request, "users/index.html")
	
def register(request):
	if request.method == "GET":
		print("index: Something went really wrong!")
		messages.error(request, "Invalid GET method used in registration request.")
		return render(request, "/users")
	else:
		print("register: Post request")
		form_valid = validation()
		errors = form_valid.registerForm(request.POST)
		if len(errors) > 0: # If any validation errors are returned user to kicked back to index w/ messages
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/users")
		process_db = database()
		checkEmail = process_db.findEmail(request.POST['email'])
		if checkEmail == True: # Check if provided e-mail already exists in database. Returns true if e-mail exists.
			print("register: E-mail address already in database.")
			messages.error(request, "The provided e-mail address is already taken.")
			return redirect("/users")
		else:
			makeUser = process_db.createUser(request.POST)
			if 'uid' in makeUser: # Login function returns dictionary with UID if login was successful
				request.session['uid'] = makeUser['uid']
				request.session['fname'] = makeUser['fname']
				request.session['lname'] = makeUser['lname']
				print("login: Successful login!")
				return redirect("/quotedash")
			for key, value in makeUser.items():
				return redirect("/users")

def login(request):
	if request.method == "GET":
		print("index: Something went really wrong!")
		messages.error(request, "Invalid GET method used in registration request.")
		return redirect("/users")
	else:
		print("login: Post request")
		form_valid = validation()
		errors = form_valid.loginForm(request.POST)
		if len(errors) > 0: # If any validation errors are returned user to kicked back to index w/ messages
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/users")
		process_db = database()
		checkEmail = process_db.findEmail(request.POST['email'])
		if checkEmail == False: # Check if provided e-mail already exists in database. Returns true if e-mail exists.
			print("login: E-mail address not in database.")
			messages.error(request, "The provided e-mail address is not in the database.")
			return redirect("/users")
		login = process_db.loginUser(request.POST)
		if 'uid' in login: # Login function returns dictionary with UID if login was successful
			request.session['uid'] = login['uid']
			request.session['fname'] = login['fname']
			request.session['lname'] = login['lname']
			print("login: Successful login!")
			return redirect("/quotedash")
		else:
			for key, value in login.items():
				messages.error(request, value)
				return redirect("/users")

def logout(request):
	if not 'uid' in request.session: # No user session, kick them out
		print("Session not found.")
		messages.error(request, "You can't log out if you aren't logged in, hotshot.")
		return redirect("/users")
	else:
		del request.session['uid']
		del request.session['fname']
		del request.session['lname']
		print("Logged out.")
		messages.error(request, "You have been logged out.")
		return redirect("/users")
	
def edit(request):
	if not 'uid' in request.session: # No user session, kick them out
		print("Session not found.")
		messages.error(request, "You must log in first!")
		return redirect("/users")
	print("edit: Edit request")
	dbQuery = users.objects.get(id=request.session['uid'])
	context = {
		"user": dbQuery
	}
	return render(request, "users/edit.html", context)

def saveEdit(request):
	if request.method == "GET":
		print("saveEdit: Something went really wrong!")
		messages.error(request, "Invalid GET method used in registration request.")
		return render(request, "/users")
	else:
		print("saveEdit: Profile edit request")
		form_valid = validation()
		errors = form_valid.registerForm(request.POST)
		if len(errors) > 0: # If any validation errors are returned user to kicked back to index w/ messages
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/users/edit")					
		# checkEmail = process_db.findEmail(request.POST['email'])   NOTE: Don't have time to make this work
		# if checkEmail == True: # Check if provided e-mail already exists in database. Returns true if e-mail exists.
			# print("register: E-mail address already in database.")
			# messages.error(request, "The provided e-mail address is already taken.")
			# return redirect("/users/edit")
		process_db = database()
		updateDict = {
			"first_name": request.POST['first_name'],
			"last_name": request.POST['last_name'],
			"email": request.POST['email'],
			"password": request.POST['password'],
			"userid": request.session['uid']
		}
		errors = process_db.updateUser(updateDict)
		if len(errors) > 0: # If any validation errors are returned user to kicked back to index w/ messages
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/users/edit")
		print("saveEdit: User profile updated!")
		messages.error(request, "User profile updated!")
		return redirect("/quotedash")
