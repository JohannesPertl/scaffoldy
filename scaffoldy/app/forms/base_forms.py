from django import forms


class FoldoutForm(forms.Form):
    active = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['active'].label = self.label

    def clean(self):
        cleaned_data = super(FoldoutForm, self).clean()
        required_fields_cleaned = [cleaned_data.get(x) for x in self.required_fields]
        if cleaned_data.get("active") and not all(x for x in required_fields_cleaned):
            missing_fields = [x for x in self.required_fields if not cleaned_data.get(x)]
            raise forms.ValidationError({x: "This field is required." for x in missing_fields})

        return cleaned_data
