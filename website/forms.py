from django import forms
from .models import User, Document
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'function','email','email_bureau', 'office_number', 'phone_number', 'city','adress_link', 'photo','website']
        
    

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'pdf']


from django.contrib.auth.forms import PasswordResetForm



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Ancien mot de passe", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmez le nouveau mot de passe", widget=forms.PasswordInput)
    
    
    
"""

class CustomSetPasswordForm(SetPasswordForm):
   
    new_password1 = forms.CharField(label=_("Nouveau mot de passe"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Confirmez le nouveau mot de passe"), widget=forms.PasswordInput)
"""