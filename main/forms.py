from .models import Name
from django import forms

class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
