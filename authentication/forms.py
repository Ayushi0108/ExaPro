from django import forms
from .models import UserProf

class UserProfForm(forms.ModelForm):
    class Meta:
        model = UserProf
        fields = "__all__"