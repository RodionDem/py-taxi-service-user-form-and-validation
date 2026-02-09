from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


def validate_license(value):
    if len(value) != 8:
        raise ValidationError("License must contain exactly 8 characters.")

    if not value[:3].isalpha() or not value[:3].isupper():
        raise ValidationError(
            "First 3 characters must be uppercase letters."
        )

    if not value[3:].isdigit():
        raise ValidationError(
            "Last 5 characters must be digits."
        )


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license])

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
