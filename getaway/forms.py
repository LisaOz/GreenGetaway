# 🔹 Custom form for event display with date and time
# getaway/forms.py
from django import forms
from .models import TripEvent

class TripEventForm(forms.ModelForm):
    class Meta:
        model = TripEvent
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'time': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        max_places = cleaned_data.get('max_places')
        booked_places = cleaned_data.get('booked_places')
        if booked_places and max_places and booked_places > max_places:
            raise forms.ValidationError(
                f"Booked places ({booked_places}) cannot exceed maximum places ({max_places})."
            )
        return cleaned_data