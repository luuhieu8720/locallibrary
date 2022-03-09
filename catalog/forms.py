from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from . import constants

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text=_("Enter a date between now and 4 weeks (default 3)."))

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=constants.VALIDATE_WEEKS):
            raise ValidationError(_('Invalid date - renewal more than {0} weeks ahead'.format(constants.VALIDATE_WEEKS)))

        return data
