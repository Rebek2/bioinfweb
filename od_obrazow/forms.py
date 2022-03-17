from django import forms
from .models import MultiMedia

class MultiMediaForm(forms.ModelForm):
    """"Form for multimedia"""
    class Meta:
        model = MultiMedia
        fields = ('title', 'image')