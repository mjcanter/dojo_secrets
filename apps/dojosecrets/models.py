# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Users(models.Model):
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	email = models.CharField(max_length=38)
	pw_hash = models.CharField(max_length=225)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __unicode__(self):
		return "id: " + str(self.id) + ", email: " + self.email

class Secrets(models.Model):
	secret_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user_id = models.ForeignKey(Users, related_name="user_secrets")

class Likes(models.Model):
	user_likes = models.ForeignKey(Users, related_name="user_likes")
	secret_likes = models.ForeignKey(Secrets, related_name="secret_likes")






	def __unicode__(self):
		return "id: " + str(self.id) + ", email: " + self.email


