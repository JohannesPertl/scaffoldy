from django import forms


class ClickhouseForm(forms.Form):
    clickhouse = forms.BooleanField(label="Clickhouse", required=False)


class ElasticsearchForm(forms.Form):
    elasticsearch = forms.BooleanField(label="Elasticsearch", required=False)


class MailhogForm(forms.Form):
    mailhog = forms.BooleanField(label="Mailhog", required=False)
