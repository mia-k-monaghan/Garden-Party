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
        # widgets = {
        #     'street_address':forms.TextInput(attrs={'id':'street'}),
        #     'apartment_address':forms.TextInput(attrs={'id':'apt','required':False}),
        #     'city':forms.TextInput(attrs={'id':'city'}),
        #     'state':forms.TextInput(attrs={'id':'state'}),
        #     'zip':forms.TextInput(attrs={'id':'zip'}),
        # }
    # shipping_street_address = forms.CharField(
    #     label="Street")
    # shipping_apartment_address = forms.CharField(
    #     required=False,
    #     label = "Apartment/Building")
    # shipping_city = forms.CharField(
    #     required=False,
    #     label = "City")
    # shipping_state = USStateField(
    #     label='State')
    # shipping_zip = USZipCodeField(
    #     label='Zip Code')
    # billing_street_address = forms.CharField(
    #     label="Street")
    # billing_apartment_address = forms.CharField(
    #     required=False,
    #     label = "Apartment/Building")
    # billing_city = forms.CharField(
    #     required=False,
    #     label = "City")
    # billing_state = USStateField(
    #     label='State')
    # billing_zip = USZipCodeField(
    #     label='Zip Code')

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
            # Fieldset(
            # 'Billing',
            # 'billing_street_address',
            # 'billing_apartment_address',
            # Row(
            #     Column('billing_city', css_class='form-group col-md-6 mb-0'),
            #     Column('billing_state', css_class='form-group col-md-4 mb-0'),
            #     Column('billing_zip', css_class='form-group col-md-2 mb-0'),
            #     css_class='form-row'
            #     ),
            # )
        )
        self.helper.form_id = 'payment-form'
        self.helper.form_method = 'POST'
        self.helper.form_action = '{% url "core:payment-complete"%}'
        self.helper.disable_csrf = True
        self.helper.form_tag = False
