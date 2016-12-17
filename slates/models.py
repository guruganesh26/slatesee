from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from user_manager import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
	
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'user_name'

	user_name = models.EmailField(blank=False, unique=True, max_length=200)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	parent_name = models.CharField(max_length=200, null=True)
	reg_no = models.IntegerField(null=True)
	mobile_no = models.CharField(max_length=12, null=True)
	password = models.CharField(max_length=50)
	profile_image = models.CharField(max_length=500)
	dob = models.DateField(null=True)
	standard = models.CharField(max_length=10, null=True)
	user_type = models.CharField(max_length=10)
	is_admin = models.BooleanField(default=False)
	created_by = models.ForeignKey('self', null=True, related_name="u_created_by")
	updated_by = models.ForeignKey('self', null=True, related_name="u_updated_by")
	teacher_id = models.ForeignKey('self', null=True, related_name="u_teacher_id")
	updated_at = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)

	objects = UserManager()

	def get_full_name(self):
		full_name = '%s %s'%(self.first_name, self.last_name)
		return full_name.strip()

	def check_password(self, password):
		if self.password == password:
			return True
		return False


class UserSession(models.Model):
	session_token =  models.CharField(primary_key=True, max_length=50)
	user_id = models.ForeignKey(User)
	session_type = models.CharField(max_length=10, default="web")
	last_accessed_time = models.DateTimeField(auto_now_add=True)

class Subject(models.Model):
	s1 = models.CharField(max_length=10)
	s2 = models.CharField(max_length=10)
	s3 = models.CharField(max_length=10)
	s4 = models.CharField(max_length=10)
	s5 = models.CharField(max_length=10)

class Marks(models.Model):
	user_id = models.ForeignKey(User, related_name='m_user_id')
	s1 = models.IntegerField()
	s2 = models.IntegerField()
	s3  = models.IntegerField()
	s4 = models.IntegerField()
	s5 = models.IntegerField()
	exam_name = models.CharField(max_length=50)
	updated_by = models.ForeignKey(User, null=True, related_name="mark_updated_by")
	updated_at = models.DateTimeField(auto_now_add=True)

class Messages(models.Model):
	message = models.TextField()
	message_type = models.CharField(max_length=20)
	is_approved = models.BooleanField(default=False)
	updated_by = models.ForeignKey(User, null=True, related_name="m_updated_by")
	created_by = models.ForeignKey(User, null=True, related_name="m_created_by")
	updated_at = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(auto_now_add=True)

class Events(models.Model):
	image_url = models.CharField(max_length=250)
	event_detail = models.TextField()
	organizer = models.ForeignKey(User, null=True, related_name="organizer")
	event_date = models.DateField()
	updated_by = models.ForeignKey(User, null=True, related_name="e_updated_by")
	created_by = models.ForeignKey(User, null=True, related_name="e_created_by")
	updated_at = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
		

class School(models.Model):
	school_name = models.CharField(max_length=150)
	principal = models.ForeignKey(User, null=True, related_name="s_principal")
	updated_at = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	no_of_students = models.IntegerField()
	no_of_teachers = models.IntegerField()
	created_by = models.ForeignKey(User, null=True, related_name="s_created_by")
	updated_by = models.ForeignKey(User, null=True, related_name="s_updated_by")
	disk_space = models.DecimalField(decimal_places=5, max_digits=40)
	disk_space_used = models.DecimalField(default=0.0, decimal_places=5, max_digits=40)

class FlashCard(models.Model):
	side_a = models.TextField()
	side_b = models.TextField()
	is_approved = models.BooleanField(default=False)
	updated_by = models.ForeignKey(User, null=True, related_name="f_updated_by")
	created_by = models.ForeignKey(User, null=True, related_name="f_created_by")
	updated_at = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(auto_now_add=True)

class McqSets(models.Model):
	set_name = models.CharField(blank=False, unique=True, max_length=250)
	is_approved = models.BooleanField(default=False)
	updated_by = models.ForeignKey(User, null=True, related_name="set_updated_by")
	created_by = models.ForeignKey(User, null=True, related_name="set_created_by")
	updated_at = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(auto_now_add=True)

class MCQ(models.Model):
	question = models.TextField()
	option1 = models.TextField()
	option2 = models.TextField()
	option3 = models.TextField()
	option4 = models.TextField()
	answer = models.CharField(max_length=10, default="option2")
	correct_text = models.TextField(null=True)
	wrong_text = models.TextField(null=True)
	set_id = models.ForeignKey(McqSets) 

		



