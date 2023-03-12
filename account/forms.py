from django import forms
from django.contrib.auth.models import User


def widget(placeholder):
    return {"class": "u-full-width", "placeholder": placeholder}


def formContent(widget, label="", max_length=64):
    return {"widget": widget, "label": label, "max_length": max_length}


class LoginForm(forms.Form):

    username = forms.CharField(
        **formContent(widget=forms.TextInput(attrs=widget("Username")))
    )
    password = forms.CharField(
        **formContent(widget=forms.PasswordInput(attrs=widget("Password")))
    )

    def clean(self):
        if self.errors:
            return self.cleaned_data

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise forms.ValidationError("Incorrect username/password.")

        return self.cleaned_data


class RegistrationForm(forms.Form):

    username = forms.CharField(
        **formContent(widget=forms.TextInput(attrs=widget("Username")))
    )

    email = forms.EmailField(
        **formContent(widget=forms.TextInput(attrs=widget("Email")))
    )

    password = forms.CharField(
        **formContent(widget=forms.PasswordInput(attrs=widget("Password")))
    )

    password_confirmation = forms.CharField(
        **formContent(
            widget=forms.PasswordInput(attrs=widget("Password confirmation"))
        )
    )

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        checkIfUserExists= User.objects.filter(username= self.cleaned_data.get("username")).exists()

        if checkIfUserExists:
            raise forms.ValidationError("Username already exists. Please choose another username!")

        if password and password != password_confirmation:
            raise forms.ValidationError("Passwords aren't matching")

        return self.cleaned_data
