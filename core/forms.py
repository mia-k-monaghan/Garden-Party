from django import forms
from .models import Address
from localflavor.us.forms import USStateField, USZipCodeField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Row, Column


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'street_address',
            'apartment_address',
            'city',
            'state',
            'zip',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
            'Shipping',
            'street_address',
            'apartment_address',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
                ),
            ),
        )
        self.fields['apartment_address'].required = False
        self.helper.form_id = 'shippinng-form'
        self.helper.form_method = 'POST'
        self.helper.disable_csrf = True
        self.helper.form_tag = False
