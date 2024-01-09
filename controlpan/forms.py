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