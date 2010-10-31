from django import forms
from panappticon import models

class EditApplicationUserForm(forms.ModelForm):
    class Meta:
        model = models.ApplicationUser
        fields = ('name', 'notes',)
