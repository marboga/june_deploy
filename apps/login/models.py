from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
import hmac
from django.utils import timezone

PASSWORD_REGEX = r'^.*\d+.*[A-Z]+.*$|^.*[A-Z]+.*\d+.*$'
EMAIL_REGEX = r'^[a-zA-Z0-9_+-]+@[a-zA-Z0-9-_+]+.[a-zA-Z]+$'

# Create your models here.
class UserManager(models.Manager):
	def validate_registration(self, data):
		errors = []
		if data['first_name']:
			if not len(data['first_name']) >= 2:
				errors.append('first name must be at least two characters!')
			if not data['first_name'].isalpha():
				errors.append('first name must contain only letters!')
		else:
			errors.append('first name must be filled!')

		if data['email']:
			if not re.match(EMAIL_REGEX, data['email']):
				errors.append('email must be valid')
		else:
			errors.append('email cannot be empty!')

		if data['last_name']:
			if not len(data['last_name']) >= 2:
				errors.append('last name must be at least two characters!')
			if not data['last_name'].isalpha():
				errors.append('last name must contain only letters!')
		else:
			errors.append('last name must be filled!')

		if data['password']:
			if not len(data['password']) >= 8:
				errors.append('password must be at least 8 characters!')
			if not re.match(PASSWORD_REGEX, data['password']):
				errors.append('password gotta include number and upper case letter')
		else:
			errors.append('password must be filled out, be at least 8 characters, contain at least one numeral and one upper case letter!')

		if not data['confirm_password'] or data['password'] != data['confirm_password']:
			errors.append('password confirmation must exist and match exactly with password')

		if errors:
			return (False, errors)
		else:
			password = data['password'].encode()
			print type(password)
			hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
			user = User.objects.create(
				first_name=data['first_name'],
				last_name=data['last_name'],
				email=data['email'],
				password=hashed_pw
			)
			return (True, user)

	def validate_login(self, data):
		print data
		errors = []
		if data['email']:
			if not re.match(EMAIL_REGEX, data['email']):
				errors.append('email not valid!')
		else:
			errors.append('email is empty!')

		if data['password']:
			if not re.match(PASSWORD_REGEX, data['password']):
				errors.append('not a valid password')
		else:
			errors.append('password is empty!')

		if errors:
			# we didn't even query the database
			return (False, errors)
		else:
			try:
				user_in_db = self.get(email=data['email'])
				raw = data['password'].encode()
				hashed = user_in_db.password.encode()

				print hashed, raw
				print type(raw), type(hashed)

				if bcrypt.hashpw(raw, hashed) == hashed:
					#user found
					return (True, user_in_db)

			except:
				print 'something failed', user_in_db


		#we had an error. Either user wasn't found or we got a bad password
		errors.append('no user with matching email/password combination found in the database')
		return (False, errors)


class User(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()
