from django import forms
from django.core.validators import FileExtensionValidator
import datetime as dt


class CSVForm(forms.Form):
    file = forms.FileField(
        label="",
        widget=forms.FileInput(
            attrs={
                "id": "file-input",
                "class": "form-control w-75",
                "accept": ".csv",
                "required": "true",
            }
        ),
        required=True,
        validators=[FileExtensionValidator(["csv"])],
    )


class TickerInput(forms.Form):
    ticker = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control fs-1 text-center py-0",
            }
        ),
    )


class DateInput(forms.Form):
    startDate = forms.DateField(
        label="Initial date",
        widget=forms.DateInput(
            attrs={
                "name": "start_date",
                "form": "ticker_form",
                "type": "date",
                "max": str(dt.date.today()),
                "class": "form-control w-75",
                "placeholder": "Enter the starting date of the stock price history",
                "required": "False",
            }
        ),
    )

    endDate = forms.DateField(
        label="Final date",
        widget=forms.DateInput(
            attrs={
                "name": "end_date",
                "form": "ticker_form",
                "type": "date",
                "max": str(dt.date.today()),
                "class": "form-control w-75",
                "placeholder": "Enter the ending date of the stock price history",
                "required": "False",
            }
        ),
    )
