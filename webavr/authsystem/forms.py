from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    #email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password2"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    def clean(self):
        # Add in custom validation here:
        # Check that the two password entries match
        cleaned_data = super(UserCreationForm,self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")
        if password1 and password2 and username:
            if password1 == password2:
                if len(password2) < 8:
                    self.add_error('password1', "Your password is too short (must be > 8 characters).")
                if "@" not in username:
                    self.add_error('username', "Email not in correct format (user@example.com).")
            else:
                self.add_error('password2', "Your passwords do not match.")


class CustomChangePassword(forms.ModelForm):
    username = forms.CharField(widget=forms.HiddenInput)
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="New Password Confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password1', 'password2', 'username']

    def save(self, commit=True):
        user = User.objects.get(id=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

    def clean(self):
        # Check that the two password entries match
        cleaned_data = super(CustomChangePassword,self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        print password2
        print password1
        if password1 and password2:
            if password1 == password2:
                if len(password2) < 8:
                    self.add_error('password1', "Your password is too short (must be > 8 characters).")
            else:
                self.add_error('password2', "Your passwords do not match.")