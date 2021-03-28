from django import forms


class DocumentForm(forms.Form):
    title = forms.CharField(max_length=255)
    file = forms.FileField(label='Select a file')
