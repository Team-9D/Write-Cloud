from django import forms
from django.contrib.auth.models import User
from .models import *


class DocumentForm(forms.ModelForm):

    docfile = forms.FileField(
        label='Select a file',
    )


class ReviewForm(forms.ModelForm):

    stars = forms.IntegerField(widget=forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]))
    body = forms.CharField(widget=forms.Textarea)

    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    story = forms.ModelChoiceField(queryset=Story.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ('stars', 'body', 'author', 'story')

