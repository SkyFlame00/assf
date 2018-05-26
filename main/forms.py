from django import forms
from django.contrib.auth.hashers import make_password

from .models import *


class Login(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation and password != None:
            raise forms.ValidationError('pass: %s, pass_conf: %s' % (password, password_confirmation))


class UniversityForm(forms.ModelForm):

    class Meta:
        model = University
        exclude = ('user', 'verified')


class CompanyForm(forms.ModelForm):
    foundation_year = forms.CharField(required=False)

    class Meta:
        model = Company
        exclude = ('user', 'verified')

    # Clean method is as the same as in UserForm
    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation and password != None:
            raise forms.ValidationError('pass: %s, pass_conf: %s' % (password, password_confirmation))


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ('user',)


class StudentEducationForm(forms.ModelForm):

    class Meta:
        model = StudentEducation
        exclude = ('student',)


class StudentJobForm(forms.ModelForm):

    class Meta:
        model = StudentJob
        exclude = ('student',)


class AddProgramForm(forms.ModelForm):

    class Meta:
        model = UniversityProgram
        exclude = ('competencies', 'university')


class AddProgramCompetencyForm(forms.Form):
    competency = forms.IntegerField(widget=forms.HiddenInput())


class StudentAdditionalCompetencyForm(forms.Form):
    competency = forms.IntegerField(widget=forms.HiddenInput())


class AddVacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        exclude = ('company', 'competencies')


class AddVacancyCompetencyForm(forms.Form):
    competency = forms.IntegerField(widget=forms.HiddenInput())


class VerifyStudentForm(forms.ModelForm):
    num = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = StudentEducation
        fields = ('verified', 'num')


class VerifyStudentJobForm(forms.ModelForm):
    num = forms.IntegerField(widget=forms.HiddenInput())
    #verified = forms.BooleanField(required=False)

    class Meta:
        model = StudentJob
        fields = ('verified', 'num')


class VerifyStudentCompetenciesForm(forms.Form):
    num = forms.IntegerField(widget=forms.HiddenInput())
    verified = forms.BooleanField(required=False)


class SearchForm(forms.Form):
    text = forms.CharField(max_length=100)

    CHOICES = (
        ('head', 'Искать в заголовках'),
        ('descr', 'Искать в описаниях')
    )

    select = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
