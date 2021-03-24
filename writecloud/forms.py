from django import forms
from django.contrib.auth.models import User
from .models import *

class RatingForm(forms.ModelForm):

    value = forms.IntegerField(widget=forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]))
    comment = forms.CharField(widget=forms.Textarea)
    
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    story = forms.ModelChoiceField(queryset=Story.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = Rating
        fields = ('value', 'comment', 'user', 'story')
