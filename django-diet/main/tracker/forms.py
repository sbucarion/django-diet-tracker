from django.forms import ModelForm
from .models import Log

class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = ['calorie', 'protein', 'fats', 'carbs', 'quantity']


class DisplayForm(ModelForm):
    None