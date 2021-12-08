from django import forms
from django.utils.safestring import mark_safe

from .base_forms import FoldoutForm


class RabbitMQForm(FoldoutForm):
    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(
        label="Password",
        help_text=mark_safe("This password is not saved and will only be used for generating the docker-compose.yml file. <br> For security reasons, you should change it in production."),
        required=False
    )
    management = forms.BooleanField(
        label="Include management plugin",
        help_text="""
        The RabbitMQ management plugin provides an HTTP-based API for management and monitoring 
        of RabbitMQ, along with a browser-based UI and a command line tool
        """,
        required=False
    )

    label = "RabbitMQ"
    prefix = "rabbitmq"
    required_fields = ['username', 'password']


class NatsForm(forms.Form):
    nats = forms.BooleanField(label="NATS", required=False)


class KafkaForm(forms.Form):
    kafka = forms.BooleanField(label="Kafka", required=False)
