
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    #email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

    def clean(self):
        # Check that the two password entries match
        cleaned_data = super(UserCreationForm,self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")
        if password1 and password2 and username:
            if password1 and password2 and password1 != password2:
                if len(password2) < 8:
                    self.add_error('password1', "Your password is too short (must be > 8 characters).")
                if "@" not in username:
                    self.add_error('username', "Email not in correct format (user@example.com).")