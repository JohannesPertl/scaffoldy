from django import forms
from django.utils.safestring import mark_safe


class ProjectNameForm(forms.Form):
    project_name = forms.CharField(
        label='Project name',
        max_length=127,
        help_text="Used on containers and folders"
    )


class ProgrammingLanguageForm(forms.Form):
    programming_language_choices = (
        ("python", "Python"),
        ("node", "Node.js"),
        ("other", "Other/None"),
    )
    programming_language = forms.ChoiceField(
        label="Programming language",
        choices=programming_language_choices,
        help_text="Used for main app container, code examples and .gitignore"
    )


class GenerateCodeExamplesForm(forms.Form):
    generate_code_examples = forms.BooleanField(
        label='Generate code examples',
        help_text="Include code examples that show how to interact with the selected services",
        required=False,
        initial=True
    )


class GitForm(forms.Form):
    repo = forms.BooleanField(
        label=mark_safe('Initialize a git repository'),
        required=False,
        initial=True
    )
    gitignore = forms.BooleanField(
        label=mark_safe('Create a <em>.gitignore</em> file'),
        help_text=mark_safe("Uses <a href='https://gitignore.io' target='_blank' rel='noreferrer' class='text-success'>gitignore.io</a>"),
        required=False,
        initial=True
    )
