from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from blogpost.models import *
from django.contrib.auth import login

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label="Password", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'password')

	def save(self, request):
		loguser = authenticate(username=self.cleaned_data['username'], password = self.cleaned_data['password'])
		if loguser:
			login(request, loguser)			


	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(username=username, password=password):
				raise forms.ValidationError("Invalid Login")
			


class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		
		def clean_email(self):
			email = self.cleaned_data['email'].lower()
			try:
				user = User.object.get(email=email)
			except Exception as e:
				return email
			raise forms.ValidationError(f"Email {email} is already in use.")

		def clean_username(self):
			username = self.cleaned_data['username']
			try:
				user = User.object.get(username=username)
			except Exception as e:
				return username
			raise forms.ValidationError(f"Username {username} is already in use.")
