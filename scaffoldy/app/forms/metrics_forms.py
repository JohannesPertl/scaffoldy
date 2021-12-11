from django import forms
from django.utils.safestring import mark_safe

from .base_forms import FoldoutForm
from hashlib import sha256


class GrafanaForm(FoldoutForm):
    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(label="Password", help_text=mark_safe("This password is not saved and will only be used for generating the docker-compose.yml file. <br> For security reasons, you should change it in production."), required=False)

    label = "Grafana"
    prefix = "grafana"
    required_fields = ['username', 'password']


class PrometheusForm(forms.Form):
    prometheus = forms.BooleanField(label="Prometheus", required=False)


class GraylogForm(FoldoutForm):
    password_secret = forms.CharField(
        label="Password secret",
        help_text="Must be at least 16 characters",
        required=False
    )
    password = forms.CharField(
        label="Password",
        help_text=mark_safe("This password is not saved and will only be used for generating the docker-compose.yml file. <br> For security reasons, you should change it in production."),
        required=False
    )
    label = "Graylog"
    prefix = "graylog"
    required_fields = ['password_secret', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password_secret = cleaned_data.get('password_secret')
        password = cleaned_data.get('password')

        if password_secret and len(password_secret) < 16:
            raise forms.ValidationError({'password_secret': "Must be at least 16 characters."})

        if password:
            hashed_password = sha256(password.encode('utf-8')).hexdigest()
            cleaned_data['hashed_password'] = hashed_password

        return cleaned_data
