import time

from bootstrap_modal_forms.generic import BSModalCreateView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import *
from .generator.logic import process_data


class FeedbackFormView(BSModalCreateView):
    template_name = 'create_feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('home')


class OnlyTextFeedbackFormView(FeedbackFormView):
    form_class = OnlyTextFeedbackForm


class GeneralFeedbackFormView(FeedbackFormView):
    form_class = GeneralFeedbackForm

class DatabasesFeedbackFormView(FeedbackFormView):
    form_class = DatabasesFeedbackForm


class MessagingFeedbackFormView(FeedbackFormView):
    form_class = MessagingFeedbackForm


class CachingFeedbackFormView(FeedbackFormView):
    form_class = CachingFeedbackForm


class MetricsFeedbackFormView(FeedbackFormView):
    form_class = MetricsFeedbackForm


class MiscFeedbackFormView(FeedbackFormView):
    form_class = MiscFeedbackForm


class DownloadFeedbackFormView(FeedbackFormView):
    form_class = DownloadFeedbackForm


def feedback(request):
    if request.method == 'GET':
        return HttpResponse(200)


def get_form_classes():
    # List of all Form classes used in view
    forms = dict(
        project_name_form=ProjectNameForm,
        programming_language_form=ProgrammingLanguageForm,
        generate_code_examples_form=GenerateCodeExamplesForm,
        git_form=GitForm,
        mysql_form=MySQLForm,
        mariadb_form=MariaDBForm,
        postgres_form=PostgreSQLForm,
        mongodb_form=MongoDBForm,
        rabbitmq_form=RabbitMQForm,
        # kafka_form=KafkaForm,
        nats_form=NatsForm,
        memcached_form=MemcachedForm,
        redis_form=RedisForm,
        grafana_form=GrafanaForm,
        prometheus_form=PrometheusForm,
        clickhouse_form=ClickhouseForm,
        elasticsearch_form=ElasticsearchForm,
        mailhog_form=MailhogForm,
        graylog_form=GraylogForm
    )
    return forms


def home(request):
    form_classes = get_form_classes()
    anchor = ""
    if request.method == 'POST':
        # Fill all forms with post
        form_classes = {form_name: form(request.POST) for form_name, form in form_classes.items()}

        for form_name, form in form_classes.items():
            if not form.is_valid():
                anchor = form_name.removesuffix('_form')
                break

        if all(form.is_valid() for form in form_classes.values()):
            # Process data
            time.sleep(1)  # Fake loading time for UX
            return process_data(request, form_classes)

    context = form_classes
    if anchor:
        context['anchor'] = anchor

    context['feedback_popovers'] = ['Miss something?', 'Any complaints?',
                                    mark_safe("Found a bug? <i class='fas fa-bug'></i>"),
                                    'Have an idea?', 'Miss a feature?', 'Need some help?',
                                    'Confused?'
                                    ]

    return render(request, 'home.html', context=context)
