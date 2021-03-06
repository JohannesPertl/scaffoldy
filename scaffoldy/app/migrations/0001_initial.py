# Generated by Django 3.2.10 on 2021-12-11 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip_address', models.CharField(blank=True, max_length=127, null=True)),
                ('session_id', models.CharField(blank=True, max_length=127, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('section', models.CharField(choices=[('general', 'General'), ('git', 'Git'), ('databases', 'Databases'), ('messaging', 'Messaging'), ('caching', 'Caching'), ('metrics', 'Metrics'), ('misc', 'Misc')], default='general', help_text='Should be set in form class, not by user', max_length=127, verbose_name='Section')),
                ('profession', models.CharField(blank=True, help_text="What's your field of work?", max_length=127, null=True, verbose_name='Your profession (Optional)')),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Your age (Optional)')),
                ('years_of_experience', models.PositiveSmallIntegerField(blank=True, help_text='How many years of experience do you roughly have in software development?', null=True, verbose_name='Years of experience (Optional)')),
                ('section_rating', models.PositiveSmallIntegerField(blank=True, choices=[(4, 'Extremely useful'), (3, 'Very useful'), (2, 'Somewhat useful'), (1, 'Slightly useful'), (0, 'Not at all useful')], help_text='How useful is this section for you?', null=True, verbose_name='Section rating')),
                ('website_rating', models.PositiveSmallIntegerField(blank=True, choices=[(4, 'Extremely useful'), (3, 'Very useful'), (2, 'Somewhat useful'), (1, 'Slightly useful'), (0, 'Not at all useful')], help_text='How useful is this website for you?', null=True, verbose_name='Website rating')),
                ('other', models.TextField(default='', help_text='If you want me to get back to you, please include your contact information :)', verbose_name='Leave me a message')),
                ('programming_language', models.CharField(blank=True, choices=[('java', 'Java'), ('c#', 'C#'), ('c', 'C'), ('c++', 'C++'), ('go', 'Go'), ('ruby', 'Ruby'), ('rust', 'Rust'), ('other', 'Other - Please mention it below')], help_text='Which programming language do you miss most?', max_length=127, null=True, verbose_name='Programming language')),
                ('database', models.CharField(blank=True, choices=[('oracle', 'Oracle'), ('microsoft_sql_server', 'Microsoft SQL Server'), ('cassandra', 'Cassandra'), ('dynamodb', 'DynamoDB'), ('couchbase', 'Couchbase'), ('influxdb', 'InfluxDB'), ('other', 'Other - Please mention it below')], help_text='Which database do you miss most?', max_length=127, null=True, verbose_name='Database')),
                ('message_queuing', models.CharField(blank=True, choices=[('zero_mq', 'ZeroMQ'), ('lightstreamer', 'Lightstreamer'), ('celery', 'Celery'), ('kafka', 'Apache Kafka'), ('other', 'Other - Please mention it below')], help_text='Which message queuing service do you miss most?', max_length=127, null=True, verbose_name='Message Queuing')),
            ],
        ),
    ]
