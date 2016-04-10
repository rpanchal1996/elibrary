from django import forms
from django.contrib.auth.models import User
from SmarterBarter.models import UserProfile
#from SmarterBarter.models import Student, Teacher
from SmarterBarter.models import UserProfile
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('year',)



"""class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Teacher
        fields = ('username', 'first_name', 'last_name','password','email')

class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Student
        
        fields =('SAP', 'first_name', 'last_name','password','email')
        """
