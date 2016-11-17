from django import forms
from auth.models import GNUser

class UserForm(forms.ModelForm):
    username = forms.CharField(
        label = 'Username',
        min_length = 6,
        required = True,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '6-30 Characters',
            }
        )
    )
    first_name = forms.CharField(
        label = 'First Name',
        required = True,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '1-30 Characters',
            }
        )
    )
    last_name = forms.CharField(
        label = 'Last Name',
        required = True,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '1-30 Characters',
            }
        )
    )
    email = forms.CharField(
        label = 'Email',
        required = True,
        widget=forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Email address',
            }
        )
    )
    password = forms.CharField(
        label = 'Password',
        min_length = 6,
        required = True,
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '6+ Characters',
            }
        )
    )
    passwordretry = forms.CharField(
        label = 'Re-enter',
        min_length = 6,
        required = True,
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '6+ Characters',
            }
        )
    )

    class Meta:
        model = GNUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        passwordretry = cleaned_data.get("passwordretry")

        if password and passwordretry:
            if password !=passwordretry:
                msg = u"Passwords don't match"
                self._errors["password"] = self.error_class([msg])
                self._errors["passwordretry"] = self.error_class([msg])

                del cleaned_data["password"]
                del cleaned_data["passwordretry"]

        return cleaned_data
