from django import forms
from django.contrib.auth.models import User
from writecloud.models import *

class RatingForm(forms.ModelForm):

    
    
    class Meta:
        model = Rating
        fields = ('value', 'comment', 'user', 'story')
