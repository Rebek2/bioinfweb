from django import forms
from .models import Multimedia

class MultiMedia_form(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ('title', 'photos')