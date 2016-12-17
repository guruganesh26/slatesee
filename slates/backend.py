from django.conf import settings
from slates.models import User


class AuthBackEnd(object):
	
	def authenticate(self, user_name=None, password=None):
		try:
			user = User.objects.get(user_name=user_name)
			if user.check_password(password):
				return user
		except User.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			user = User.objects.get(pk=user_id)
			if user.is_active:
				return user
			return None
		except User.DoesNotExist:
			return None
