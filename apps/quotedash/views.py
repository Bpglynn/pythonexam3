from django.shortcuts import render, redirect
from apps.quotedash.models import validateQuote, quoteDatabase, quotes, quote_likes
from apps.users.models import users
from django.db.models import Count
from django import forms
from django.contrib import messages

# Create your views here.

def index(request):
	# if not 'uid' in request.session: # No user session, kick them out to users app
		# print("Session not found.")
		# messages.error(request, "You must be logged in to access this page!")
		# return redirect("/users")
	print("index: Get request")
	# Query DB to get quotes along with annotated count of likes
	dbQueryQuotes = quotes.objects.all().annotate(likeCount=Count('quote_likes')).order_by('-created_at')
	context = {
		"quotes": dbQueryQuotes,
	}
	return render(request, "quotedash/index.html", context)

def postQuote(request):
	if not 'uid' in request.session: # No user session, kick them out to users app
		print("Session not found.")
		messages.error(request, "You must be logged in to access this page!")
		return redirect("/users")
	print("postQuote: Add quote to database")
	quote1 = validateQuote() # Instantiate
	errors = quote1.validForm(request.POST)
	if len(errors) > 0: # If any validation errors are returned 
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/quotedash")
	# Build dictionary for database function
	quoteDict = {
		"quote": request.POST['quoteBody'],
		"author": request.POST['quoteAuthor'],
		"uid": request.session['uid']
	}
	quote2 = quoteDatabase() # Instantiate
	errors = quote2.addQuote(quoteDict)
	if len(errors) > 0: # If database errors are returned
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/quotedash")
	return redirect("/quotedash")

def likeQuote(request, number):
	if not 'uid' in request.session: # No user session, kick them out to users app
		print("Session not found.")
		messages.error(request, "You must be logged in to access this page!")
		return redirect("/users")
	print("likeQuote: Adding like to quote...")
	quoteDict = {
		"quote_id": number,
		"uid": request.session['uid']
	}
	quote = quoteDatabase()
	errors = quote.likeQuote(quoteDict) # Pass id of quote to be liked and UID of requesting user
	if len(errors) > 0: # If database errors are returned
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/quotedash")
	return redirect("/quotedash")
	
def deleteQuote(request, number):
	if not 'uid' in request.session: # No user session, kick them out to users app
		print("Session not found.")
		messages.error(request, "You must be logged in to access this page!")
		return redirect("/users")
	print("postQuote: Add quote to database")
	quoteDict = {
		"quote_id": number,
		"reqesting_uid": request.session['uid']
	}
	quote = quoteDatabase()
	errors = quote.deleteQuote(quoteDict) # Pass id of quote to be deleted and UID of requesting user
	if len(errors) > 0: # If database errors are returned
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/quotedash")
	return redirect("/quotedash")

def viewUser(request, number):
	# if not 'uid' in request.session: # No user session, kick them out to users app
		# print("Session not found.")
		# messages.error(request, "You must be logged in to access this page!")
		# return redirect("/users")
	print("viewUser: Getting user page and quote list.")
	dbQuery = quotes.objects.filter(user_id=number).order_by('-created_at')
	dbQuery2 = users.objects.get(id=number)
	context = {
		"quotes": dbQuery,
		"user": dbQuery2
	}
	return render(request, "quotedash/viewuser.html", context)

