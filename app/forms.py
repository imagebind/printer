# myapp/forms.py

from django import forms
from .models import Customer, State, District

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'father_name', 'cell_number', 'refer_by', 'bjp_membership_number', 'email', 
            'flat_no', 'flat_name', 'door_number', 
            'street_name', 'area', 'taluk', 
            'district', 'state', 'pincode', 
            'landmark', 'plan'
        ]
        labels = {
                    'refer_by': 'Refer By(optional)', 
                    'bjp_membership_number': 'BJP Membership Number(optional)', 
                }


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

        plans_with_prices = {
            'Plan A': 'Rs.600/-  (One Year-52 issues)',
            'Plan B': 'Rs.1500/- (Three Years-156 issues)',
            'Plan C': 'Rs.10,000/- (Life Time)'
        }
        self.fields['plan'].choices = [(key, value) for key, value in plans_with_prices.items()]
        self.fields['refer_by'].required = False 
        self.fields['bjp_membership_number'].required = False 


