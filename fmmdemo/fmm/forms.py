from django import forms
from fmm.models import Feature

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['enabled', 'selected']

