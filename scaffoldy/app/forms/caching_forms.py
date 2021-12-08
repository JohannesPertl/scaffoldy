from django import forms


class MemcachedForm(forms.Form):
    memcached = forms.BooleanField(label="Memcached", required=False)


class RedisForm(forms.Form):
    redis = forms.BooleanField(label="Redis", required=False)
