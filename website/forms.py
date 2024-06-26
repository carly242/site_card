from django import forms
from .models import User, Document
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'function', 'email', 'email_bureau', 'office_number', 'phone_number', 'city', 'adress_link', 'photo', 'website']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Changes'))
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'pdf']


from django.contrib.auth.forms import PasswordResetForm



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Ancien mot de passe", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmez le nouveau mot de passe", widget=forms.PasswordInput)
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def _init_(self, *args, **kwargs):
        super(ContactForm, self)._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Envoyer'))
    
"""

class CustomSetPasswordForm(SetPasswordForm):
   
    new_password1 = forms.CharField(label=_("Nouveau mot de passe"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Confirmez le nouveau mot de passe"), widget=forms.PasswordInput)
"""