from django import forms

class RegisterForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()
	password2 = forms.CharField()
	email = forms.EmailField(required=False)
	message = forms.CharField(required=False)
	
	def clean_password(self):
		password = self.cleaned_data['password']
		password2 = self.cleaned_data['password2']
		if password == password2:
			raise forms.ValidationError("password XXX")
		return password