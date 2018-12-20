from django.db import models
from apps.users.models import users

# Create your models here.

class validateQuote(models.Model): # Basic input validation functions
	def __init__(self):
		print("validateQuote: Object created.")
	def validForm(self, formData): # Quote form validation
		errors = {}
		if len(formData['quoteBody']) < 11:
			print("quote: Does not meet minimum length.")
			errors["quotebody1"] = "Quote must be longer than ten characters."
		if len(formData['quoteBody']) > 255:
			print("quote: Exceeds 255 characters.")
			errors["quotebody2"] = "Quote cannot be longer than 255 characters."
		if len(formData['quoteAuthor']) < 4:
			print("author: Does not meet minimum length.")
			errors["quoteauthor1"] = "Author name must be longer than three characters."
		if len(formData['quoteAuthor']) > 32:
			print("author: Exceeds 32 characters.")
			errors["quoteauthor2"] = "Author name cannot be longer than 32 characters."
		return errors

class quoteDatabase(models.Model): # Quote database options
	def __init__(self):
		print("quoteDatabase: Object created.")
	def addQuote(self, addDict):
		errors = {}
		try: # Add to database
			dbQuery = quotes.objects.create(user_id=(users.objects.get(id=addDict['uid'])), author=addDict['author'], quote=addDict['quote'])
		except:
			print("Database error when trying to add quote.")
			errors["database"] = "Database error. Please contact the administrator."
			return errors
		print("Quote added to database.")
		return errors
	def likeQuote(self, likeDict):
		errors = {}
		try:
			# Build dictionary of user ids that have likes associated with the quote id.
			# This feels like a completely stupid way to do this but I can't get it to work any other way
			getLikes = {x.user_id_id for x in quote_likes.objects.filter(quote_id_id=likeDict['quote_id']).all()}
		except:
			print("Database error when trying to get likes.")
			errors["database"] = "Database error. Please contact the administrator."
			return errors
		print(getLikes)
		if likeDict['uid'] in getLikes: # See if user id is in list returned from database. If it is that means they already liked the quote.
			print("User already liked the quote.")
			errors["likedmsg"] = "You've already liked that quote!"
			return errors
		try:
			addLike = quote_likes.objects.create(quote_id=(quotes.objects.get(id=likeDict['quote_id'])), user_id=(users.objects.get(id=likeDict['uid'])))
		except:
			print("Database error when trying to add like.")
			errors["database"] = "Database error. Please contact the administrator."
			return errors
		return errors
		
	def deleteQuote(self, delDict):
		errors = {}
		try: # Get quote from database
			dbQuery = quotes.objects.get(id=delDict['quote_id'])
		except:
			print("Database error when trying to retrieve quote for deletion.")
			errors["database"] = "Database error. Please contact the administrator."
			return errors
		if dbQuery.user_id.id != delDict['reqesting_uid']: # Check if user requesting delete is the owner of the quote
			print("User requesting quote delete does not have permission!")
			errors["security"] = "You do not have permission to delete the quote!"
			return errors
		dbQuery.delete()
		return errors
		
class quotes(models.Model):
	user_id = models.ForeignKey(users, on_delete=models.CASCADE)
	author = models.CharField(max_length=32)
	quote = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class quote_likes(models.Model):
	quote_id = models.ForeignKey(quotes, on_delete=models.CASCADE)
	user_id = models.ForeignKey(users, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)