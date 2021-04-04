from django import forms
from .models import *


# Form for reviewing a story
class ReviewForm(forms.ModelForm):

    stars = forms.IntegerField(widget=forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]))
    body = forms.CharField(widget=forms.Textarea)

    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    story = forms.ModelChoiceField(queryset=Story.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ('stars', 'body', 'author', 'story')

