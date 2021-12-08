from hashlib import sha256

from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.utils import is_ajax
from django import forms
from ipware import get_client_ip

from app.models.feedback_models import Feedback


class OnlyTextFeedbackForm(BSModalModelForm):
    class Meta:
        model = Feedback
        exclude = ['id', 'timestamp']
        widgets = {
            'other': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }
        fields = ['other']

    def save(self, commit=True):
        feedback = super().save(commit=False)

        # Section
        feedback.section = self.section

        # Get session id
        feedback.session_id = self.get_session_id()

        # Get IP address
        client_ip, is_routable = get_client_ip(self.request)
        if client_ip is not None and is_routable:
            hashed_ip = sha256(client_ip.encode('utf-8')).hexdigest()
            feedback.ip_address = hashed_ip

        if commit and not is_ajax(self.request.META) or self.request.POST.get('asyncUpdate') == 'True':
            feedback.save()
        return feedback

    def get_session_id(self):
        if not self.request.session.session_key:
            self.request.session.create()
        return self.request.session.session_key


class FeedbackForm(BSModalModelForm):
    section = "general"
    section_rating_label = "Section rating"
    section_rating_help_text = "How useful is this section for you?"

    class Meta:
        model = Feedback
        exclude = ["id", "timestamp"]
        widgets = {
            'other': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        section_rating = self.fields.get('section_rating')
        if section_rating:
            self.fields['section_rating'].label = self.section_rating_label
            self.fields['section_rating'].help_text = self.section_rating_help_text

        session_id = self.get_session_id()

        # Check if demographic data already exists in database and set it to initial data/hide it
        existing_session_feedback = Feedback.objects.filter(session_id=session_id).order_by('timestamp')
        demographic_data = dict(
            age=None,
            profession=None,
            years_of_experience=None,
        )
        for feedback in existing_session_feedback:
            for field, value in demographic_data.items():
                feedback_field = getattr(feedback, field)
                if feedback_field:
                    demographic_data[field] = feedback_field

        for field, value in demographic_data.items():
            if value:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].initial = value

    def save(self, commit=True):
        feedback = super().save(commit=False)

        # Check if feedback is empty or contains only unusable data
        d = feedback.__dict__
        useless_data = ['_state', 'id', 'ip_address', 'session_id', 'timestamp', 'section', 'profession', 'age',
                        'years_of_experience']
        if all(not value for key, value in d.items() if key not in useless_data):
            return feedback

        # Section
        feedback.section = self.section
        # Get session id
        feedback.session_id = self.get_session_id()

        # Get IP address
        client_ip, is_routable = get_client_ip(self.request)
        if client_ip is not None and is_routable:
            hashed_ip = sha256(client_ip.encode('utf-8')).hexdigest()
            feedback.ip_address = hashed_ip

        if commit and not is_ajax(self.request.META) or self.request.POST.get('asyncUpdate') == 'True':
            feedback.save()
        return feedback

    def get_session_id(self):
        if not self.request.session.session_key:
            self.request.session.create()
        return self.request.session.session_key



class GeneralFeedbackForm(OnlyTextFeedbackForm):
    section = "general"


class DatabasesFeedbackForm(OnlyTextFeedbackForm):
    section = "databases"


class MessagingFeedbackForm(OnlyTextFeedbackForm):
    section = "messaging"


class CachingFeedbackForm(OnlyTextFeedbackForm):
    section = "caching"

class MetricsFeedbackForm(OnlyTextFeedbackForm):
    section = "metrics"


class MiscFeedbackForm(OnlyTextFeedbackForm):
    section = "misc"


class DownloadFeedbackForm(OnlyTextFeedbackForm):
    section = "download"
