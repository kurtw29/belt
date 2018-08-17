from __future__ import unicode_literals
from django.db import models
import re
name_regex = re.compile(r'^[a-zA-Z\D.-]+$')
email_regex = re.compile(r'^[a-zA-Z\d.+_-]+@[a-zA-Z\d._-]+\.[a-zA-Z]+$')
pw_regex = re.compile(r'^.*(?=.*\d)(?=.*[a-zA-Z]).*$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['first_name']):
            errors['first_name'] = "First name should be letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['last_name']):
            errors['last_name'] = "Last name should be letters only"
        if len(postData['email']) < 6:
            errors['email'] = "Invalid Email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email - address format"
        elif User.objects.filter(email = postData['email']):
            errors['email'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be fewer than 8 characters"
        elif not postData['password'] == postData['confirm_password']:
            errors['password'] = "Need to match Password Confirmation"
        elif not pw_regex.match(postData['password']):
            errors['password'] = "Password needs at least one digit and one capital letter"
        return errors

    def quote_validator(self, postData):
        errors={}
        if len(postData['author_name']) < 1:
            errors['author_name'] = "Author cannot be blank"
        elif not name_regex.match(postData['author_name']):
            errors['author_name'] = "Name should be letters only"
        if len(postData['quote_content']) < 1:
            errors['quote_content'] = "Quote cannot be empty"
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['first_name']):
            errors['first_name'] = "Letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['last_name']):
            errors['last_name'] = "Last name should be letters only"
        if len(postData['email']) < 6:
            errors['email'] = "Invalid Email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email - address format"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
class Quote(models.Model):
    author = models.CharField(max_length = 255)
    quote = models.TextField()
    poster = models.ForeignKey(User, related_name = "posted_quotes")
    liked_users = models.ManyToManyField(User, related_name='liked_quotes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
