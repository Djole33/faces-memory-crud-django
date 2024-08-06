from .models import Name, Level
from django import forms

class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LevelForm(forms.Form):
    LEVEL_CHOICES = [(i, f'Level {i} ({i*2} faces)') for i in range(1, 5)]
    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Select Level")
