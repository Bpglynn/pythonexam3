from django.db import models
import re
import bcrypt

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class validation(models.Model): # Basic input validation functions
	def __init__(self):
		print("validation: Object created.")
	def loginForm(self, formData): # Login form validation
		errors = {}
		# E-mail validation
		if len(formData['email']) < 1:
			print("loginForm: No e-mail address provided.")
			errors["email1"] = "Please provide an e-mail address."
		if len(formData['email']) > 32:
			print("loginForm: E-mail address too long.")
			errors["email2"] = "E-mail address is too long. Max allowed: 32 characters."
		if not EMAIL_REGEX.match(formData['email']):
			print("email: Invalid e-mail format detected.")
			errors["email3"] = "Invalid e-mail format."
			return errors
		# Password validation
		if len(formData['password']) < 1:
			print("loginForm: No password provided.")
			errors["password1"] = "Please provide a password."
		if len(formData['password']) > 32:
			print("loginForm: Password too long.")
			errors["password2"] = "Password is too long. Max allowed: 32 characters."
		return errors
	def registerForm(self, formData): # Registration form validation
		errors = {}
		# Name validation
		if len(formData['first_name']) < 1:
			print("loginForm: No first name provided.")
			errors["first_name1"] = "Please provide a first name."
		if len(formData['first_name']) > 32:
			print("loginForm: First name too long.")
			errors["first_name2"] = "First name too long. Max allowed: 32 characters"
		if not formData['first_name'].isalnum():
			print("loginForm: First name is not alphanumeric.")
			errors["first_name3"] = "Provided first name has non-alphanumeric characters."
		if len(formData['last_name']) < 1:
			print("loginForm: No last name provided.")
			errors["last_name1"] = "Please provide a last name."
		if len(formData['last_name']) > 32:
			print("loginForm: Last name too long.")
			errors["last_name2"] = "Last name too long. Max allowed: 32 characters"
		if not formData['last_name'].isalnum():
			print("loginForm: Last name is not alphanumeric.")
			errors["last_name3"] = "Provided last name has non-alphanumeric characters."
		# E-mail validation
		if len(formData['email']) < 1:
			print("loginForm: No e-mail address provided.")
			errors["email1"] = "Please provide an e-mail address."
		if len(formData['email']) > 32:
			print("loginForm: E-mail address too long.")
			errors["email2"] = "E-mail address is too long. Max allowed: 32 characters."
		if not EMAIL_REGEX.match(formData['email']):
			print("email: Invalid e-mail format detected.")
			errors["email3"] = "Invalid e-mail format."
			return errors
		# New password validation
		if len(formData['password']) < 8: # Length
			print("loginForm: Password minimum length not met.")
			errors["password1"] = "Password must be greater than 8 characters."
		if len(formData['password']) > 32: # Length
			print("loginForm: Password too long.")
			errors["password2"] = "Password is too long. Max allowed: 32 characters."
		if len(formData['confirm_password']) > 32: 
			print("loginForm: Confirm password too long.")
			errors["password3"] = "Password confirmation is too long. Max allowed: 32 characters."
		if not re.search(r"\d", formData['password']): # Check for numeric
			print("loginForm: No numbers in password.")
			errors["password4"] = "Password must contain at least one numeric digit."
		# if re.search(r"[A-Z]", formData['password']): # Check for all upper case
			# print("loginForm: Password all upper case.")
			# errors["password5"] = "Password must contain mixed case letters."
		# if re.search(r"[a-z]", formData['password']): # Check for all lower case
			# print("loginForm: Password all lower case.")
			# errors["password6"] = "Password must contain mixed case letters."
		if formData['password'] != formData['confirm_password']: # Make sure password and confirm password fields match
			print("loginForm: Passwords do not match.")
			errors["password7"] = "Password and confirm password fields do not match."
		return errors

class database(models.Model): # Database functions
	def __init__(self):
		print("database: Object created.")
	def findEmail(self, formData): # Check if provided e-mail is in database
		errors = {}
		print("findEmail: Trying to find provided email address.")
		try:
			dbQuery = users.objects.filter(email=formData)
			print("Database query successful.")
			if not dbQuery: # Empty dictionary will evaluate as false
				print("findEmail: No existing e-mail found.")
				return False
			else: # Populated dictionary means the database returned a row with the e-mail address.
				print("findEmail: Found existing e-mail in database.")
				return True
		except:
			print("findEmail: Database query error.")
			errors["database"] = "Database error. Please contact administartor."
			return errors
	def createUser(self, formData): # Create new user account
		errors = {}
		try:
			hashedPW = bcrypt.hashpw(formData['password'].encode(), bcrypt.gensalt()) # Hash the password
			print("Password hashed.")
		except:
			print("createUser: Cryptographic error.")
			errors["bcrypt"] = "Cryptographic error. Please contact the administrator."
			return errors # Drop out of function, we can't continue without a hash
		try: # Add to database
			dbQuery = users.objects.create(first_name=formData['first_name'], last_name=formData['last_name'], email=formData['email'], passhash=hashedPW)
		except:
			print("Database error when trying to execute users.objects.create().")
			errors["database"] = "Database error. Please contact the administrator."
			return errors
		print("createUser: Added user.")
		userInfo = {
				"uid": dbQuery.id,
				"fname": dbQuery.first_name,
				"lname": dbQuery.last_name
			}
		return userInfo
	def updateUser(self, formData): # Update user account
		errors = {}
		try:
			dbQuery = users.objects.get(id=formData['userid'])
		except: 
			print("Database error when trying to get existing user in updateUser.")
			errors["database"] = "Database error. Please contact the administrator."
			return errors
		if dbQuery.email != formData['email']:
			print("User is trying to change email addresses. Check if new one exists.")
			checkEmail = database()
			email = checkEmail.findEmail(formData['email'])
			if email == True:
				print("updateUser: User tried to change email address to another already in the database.")
				errors["email"] = "The new e-mail address you provided is already in the database."
				return errors # Drop out of function, we can't continue without a hash
		try:
			hashedPW = bcrypt.hashpw(formData['password'].encode(), bcrypt.gensalt()) # Hash the password
			print("Password hashed.")
		except:
			print("updateUser: Cryptographic error.")
			errors["bcrypt"] = "Cryptographic error. Please contact the administrator."
			return errors # Drop out of function, we can't continue without a hash
		try: # Update database object
			dbQuery.first_name = formData['first_name']
			dbQuery.last_name = formData['last_name']
			dbQuery.email = formData['email']
			dbQuery.passhash = hashedPW
			dbQuery.save()
		except:
			print("Database error when trying to update user object.")
			errors["database"] = "Database error. Please contact the administrator."
			return errors
		print("updateUser: User updated.")
		return errors
	def loginUser(self, formData): # Login existing user account
		errors = {}
		try: # Get user data row
			dbQuery = users.objects.get(email=formData['email'])
			print("Database query successful.")
		except:
			print("loginUser: Database query error.")
			errors["database"] = "Database error. Please contact administartor."
			return errors
		passwordCheck = bcrypt.checkpw(formData['password'].encode(), dbQuery.passhash.encode()) # Check provided password against database hashed. Returns true or false.
		if passwordCheck == False:
			print("loginUser: Incorrect password.")
			errors["database"] = "Incorrect password."
			return errors
		else:
			userInfo = {
				"uid": dbQuery.id,
				"fname": dbQuery.first_name,
				"lname": dbQuery.last_name
			}
			print("loginUser: Good password.")
			return userInfo
			
class users(models.Model):
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	email = models.CharField(max_length=64)
	passhash = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
