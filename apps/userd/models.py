from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		name_regex = re.compile(r'^[a-zA-Z]+$')
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['fname']) < 1:
			errors['fname'] = 'First name field left blank!'
		if len(postData['lname']) < 1:
			errors['lname'] = 'Last name field left blank!'
		if not name_regex.match(postData['fname']) or not name_regex.match(postData['lname']):
			errors['letters'] = 'Letters only for names please'
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Invalid email address!'
		if len(postData['pword']) < 8:
			errors['pword'] = 'Password too short'
		if not postData['pword'] == postData['cpword']:
			errors['cpword'] = 'Passwords dont match'
		if User.objects.filter(email = postData['email'].lower()).exists():
			errors['exists'] = 'Email already used'
		if len(errors) == 0:
			pw = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
			a = User.objects.create(fname = postData['fname'], lname = postData['lname'],
				email= postData['email'].lower(), pword = pw, user_level = "normal")
			errors['id'] = a.id
			errors['user_level'] = a.user_level
			if a.id == 1:
				a.user_level = "admin"
				a.save()
		return errors

	def login_validator(self,postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['email']) < 1:
			errors['email'] = 'Email field left blank!'
		if len(postData['pword']) < 1:
			errors['pword'] = 'Password field left blank!'
		if len(errors) == 0:
			if User.objects.filter(email = postData['email']).exists():
				a = User.objects.get(email = postData['email'])
				if bcrypt.checkpw(postData['pword'].encode(), a.pword.encode()):
					errors['id'] = a.id
					errors['user_level'] = a.user_level	
				else:
					errors['credentials'] = "Wrong Credentials"
			else:
				errors['credentials'] = "Wrong Credentials"
		return errors

	def editinfo_validator(self, postData):
		name_regex = re.compile(r'^[a-zA-Z]+$')
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['fname']) < 1:
			errors['fname'] = 'First name field left blank!'
		if len(postData['lname']) < 1:
			errors['lname'] = 'Last name field left blank!'
		if not name_regex.match(postData['fname']) or not name_regex.match(postData['lname']):
			errors['letters'] = 'Letters only for names please'
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Invalid email address!'
		if User.objects.filter(email = postData['email'].lower()).exists():
			errors['exists'] = 'Email already used'
		if len(errors) == 0:
			a = User.objects.get(id = postData['uid'])
			a.email = postData['email']
			a.fname = postData['fname']
			a.lname = postData['lname']
			a.user_level = postData['ulvl']
			a.save()
			errors['success'] = "Information Saved!"
		return errors

	def editpword_validator(self, postData):
		errors = {}
		if len(postData['pword']) < 8:
			errors['pword'] = 'Password too short'
		if not postData['pword'] == postData['cpword']:
			errors['cpword'] = 'Passwords dont match'
		if len(errors) == 0:
			pw = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
			a = User.objects.get(id = postData['uid'])
			a.pword = pw
			a.save()
			errors['success'] = "Password Succesfully Saved!"
		return errors

	def editdesc_validator(self, postData):
		errors = {}
		if len(postData['desc']) < 1:
			errors['desc'] = "Description field left blank!"
		if len(errors) == 0:
			a = User.objects.get(id = postData['uid'])
			a.desc = postData['desc']
			a.save()
			errors['success'] = "Description Succesfully Saved!"
		return errors

	def delete(self, uid):
		user = User.objects.get(id = uid)
		user.delete()
		pass

	def msgvalid(self, postData):
		errors = {}
		if len(postData['msg']) < 1:
			errors['msg'] = "Message field left blank!"
		if len(errors) == 0:
			Message.objects.create(content = postData['msg'], messenger_id = postData['mid'], receiver_id = postData['rid'])
			errors['success'] = True
		return errors

	def cmntvalid(self, postData):
		errors = {}
		if postData['cmnt'] == "Add a comment" or len(postData['cmnt']) < 1:
			errors['cmnt'] = "Comment field left blank!"
		if len(errors) == 0:
			Comment.objects.create(content = postData['cmnt'], commenter_id = postData['cid'], message_id = postData['cmid'])
			errors['success'] = True
		return errors

class User(models.Model):
	fname = models.CharField(max_length = 255)
	lname = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	pword = models.CharField(max_length = 255)
	user_level = models.CharField(max_length = 255)
	desc = models.TextField(default = "")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Message(models.Model):
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	receiver = models.ForeignKey(User, related_name= "received_msgs")
	messenger = models.ForeignKey(User, related_name = "messages")

class Comment(models.Model):
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	commenter = models.ForeignKey(User, related_name = "comments")
	message = models.ForeignKey(Message, related_name = "comments")
		