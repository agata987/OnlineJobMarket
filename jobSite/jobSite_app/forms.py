from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, JobOffer
from jobSite_app.choices import *

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','first_name','last_name',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są identyczne.")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
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
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'is_job_seeker','is_employee','description')


class CreateJobOffer(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = {"name","company","full_time","remote","description","max_salary","min_salary"}

class CreateOfferForm(forms.Form):
    name = forms.CharField(label = "Stanowisko:", max_length=100)
    company = forms.CharField(label = "Firma:", max_length=100,required=False)
    category = forms.ChoiceField(label="Kategoria:",choices=CATEGORY_CHOICES,widget=forms.Select(),initial=22)
    full_time = forms.BooleanField(label="Pełny etat:",initial=True,required=False)
    remote = forms.BooleanField(label="Zdalnie:",initial=False,required=False)
    description = forms.CharField(label = "Opis:", widget=forms.Textarea(attrs={'rows':5, 'cols':30}),required=False)
    city =  forms.ChoiceField(label="Miasto:",choices=CITY_CHOICES,widget=forms.Select(),initial="Inne")
    # country =  forms.CharField(label = "Kraj:", max_length=20,required=False)
    min_salary = forms.FloatField(label = "Min. wynagrodzenie:", max_value=10000000)
    max_salary = forms.FloatField(label = "Max. wynagrodzenie:", max_value=10000000,required=False)

class EditOfferForm(forms.Form):
    full_time = forms.BooleanField(label="Pełny etat:",initial=True,required=False)
    remote = forms.BooleanField(label="Zdalnie:",initial=False,required=False)
    description = forms.CharField(label = "Opis:", widget=forms.Textarea(attrs={'rows':5, 'cols':30}),required=False)
    min_salary = forms.FloatField(label = "Min. wynagrodzenie:", max_value=10000000)
    max_salary = forms.FloatField(label = "Max. wynagrodzenie:", max_value=10000000,required=False)