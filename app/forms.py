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
            'state', 'district',  'pincode', 
            'landmark', 'plan'
        ]
        labels = {
                    'refer_by': 'Reference by (Name)', 
                    'bjp_membership_number': 'Reference by (Cell Number)', 
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
            'Plan B': 'Rs.1000/- (Three Years-156 issues)',
            'Plan C': 'Rs.10,000/- (Life Time)'
        }
        self.fields['plan'].choices = [(key, value) for key, value in plans_with_prices.items()]
        self.fields['refer_by'].required = False 
        self.fields['bjp_membership_number'].required = False 


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)



class VerifyCustomerForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254, required=True)
    cell_number = forms.CharField(
        label="Mobile Number", 
        max_length=10, 
        required=True, 
        validators=[Customer._meta.get_field('cell_number').validators[0]]  # Use the same validator as in the model
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        cell_number = cleaned_data.get("cell_number")

        # Verify customer existence
        try:
            customer = Customer.objects.get(email=email, cell_number=cell_number)
        except Customer.DoesNotExist:
            raise forms.ValidationError("No customer found with the given email and mobile number.")
        
        cleaned_data["customer"] = customer  # Attach customer data for further use if needed
        return cleaned_data

