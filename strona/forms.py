from django import forms
from strona.models import Multimedia, Downloadable


class MultiMedia_form(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ('title', 'photos', 'members', 'gallery')

class File_to_download_form(forms.ModelForm):
    file_upload = forms.FileField()
    class Meta:
        model = Downloadable
        fields = ('name', 'upload', 'downloads')
