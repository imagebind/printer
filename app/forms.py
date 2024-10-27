# myapp/forms.py

from django import forms
from .models import Customer, State, District

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'father_name', 'cell_number', 'email', 
            'flat_no', 'flat_name', 'door_number', 
            'street_name', 'area', 'taluk', 
            'district', 'state', 'pincode', 
            'landmark', 'plan'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, you can customize initial queryset for districts based on state selection
        self.fields['district'].queryset = District.objects.none()
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.state.districts.order_by('name')
