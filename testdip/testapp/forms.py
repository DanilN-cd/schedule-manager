from django import forms
from .models import Group, Prepods, PredM

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'master', 'kurator']


class PrepodForm(forms.ModelForm):
    predmet = forms.ModelMultipleChoiceField(
        queryset=PredM.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Используем чекбоксы
        required=False
    )

    class Meta:
        model = Prepods
        fields = ['name', 'predmet', 'Cab']