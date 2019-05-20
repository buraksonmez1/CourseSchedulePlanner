from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User



class RegisterForm(forms.ModelForm):
    username    = forms.CharField(label='Student Number', required=True)
    password1   = forms.CharField(label='Campus Online Password', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Password Again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if len(username) < 6 or len(username) > 30:
            raise forms.ValidationError(self.error_messages['username_character'])
        if qs.exists():
            raise forms.ValidationError(self.error_messages['username_exists'])
        return username

    def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Password does not match!")
            return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
class LoginForm(forms.Form):
    username    = forms.CharField(label='student_no',max_length=55)
    password    = forms.CharField(label='password',max_length=55)

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label='Şifre oluşturun', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Şifrenizi onaylayın', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = {
            'username',
        }
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler eşleşmiyor")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        ),
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
