from django import forms


class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file',
    )