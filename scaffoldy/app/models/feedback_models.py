from django.db import models

other_feedback = ("other", "Other - Please mention it below")


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.CharField(
        max_length=127,
        blank=True,
        null=True
    )
    session_id = models.CharField(
        max_length=127,
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(
        auto_now=True
    )
    section = models.CharField(
        verbose_name="Section",
        help_text="Should be set in form class, not by user",
        max_length=127,
        choices=(
            ("general", "General"),
            ("git", "Git"),
            ("databases", "Databases"),
            ("messaging", "Messaging"),
            ("caching", "Caching"),
            ("metrics", "Metrics"),
            ("misc", "Misc"),
        ),
        default="general"
    )
    profession = models.CharField(
        verbose_name="Your profession (Optional)",
        help_text="What's your field of work?",
        blank=True,
        null=True,
        max_length=127
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Your age (Optional)",
        blank=True,
        null=True
    )
    years_of_experience = models.PositiveSmallIntegerField(
        verbose_name="Years of experience (Optional)",
        help_text="How many years of experience do you roughly have in software development?",
        blank=True,
        null=True
    )
    section_rating = models.PositiveSmallIntegerField(
        verbose_name="Section rating",
        help_text="How useful is this section for you?",
        choices=(
            (4, 'Extremely useful'),
            (3, 'Very useful'),
            (2, 'Somewhat useful'),
            (1, 'Slightly useful'),
            (0, 'Not at all useful')
        ),
        blank=True,
        null=True
    )
    website_rating = models.PositiveSmallIntegerField(
        verbose_name="Website rating",
        help_text="How useful is this website for you?",
        choices=(
            (4, 'Extremely useful'),
            (3, 'Very useful'),
            (2, 'Somewhat useful'),
            (1, 'Slightly useful'),
            (0, 'Not at all useful')
        ),
        blank=True,
        null=True
    )
    other = models.TextField(
        verbose_name="Leave me a message",
        help_text="If you want me to get back to you, please include your contact information :)",
        blank=False,
        null=False,
        default=""
    )
    programming_language = models.CharField(
        verbose_name="Programming language",
        help_text="Which programming language do you miss most?",
        choices=(
            ("java", "Java"),
            ("c#", "C#"),
            ("c", "C"),
            ("c++", "C++"),
            ("go", "Go"),
            ("ruby", "Ruby"),
            ("rust", "Rust"),
            other_feedback,
        ),
        blank=True,
        null=True,
        max_length=127
    )
    database = models.CharField(
        verbose_name="Database",
        help_text="Which database do you miss most?",
        choices=(
            ("oracle", "Oracle"),
            ("microsoft_sql_server", "Microsoft SQL Server"),
            ("cassandra", "Cassandra"),
            ("dynamodb", "DynamoDB"),
            ("couchbase", "Couchbase"),
            ("influxdb", "InfluxDB"),
            other_feedback,
        ),
        blank=True,
        null=True,
        max_length=127
    )
    message_queuing = models.CharField(
        verbose_name="Message Queuing",
        help_text="Which message queuing service do you miss most?",
        choices=(
            ("zero_mq", "ZeroMQ"),
            ("lightstreamer", "Lightstreamer"),
            ("celery", "Celery"),
            ("kafka", "Apache Kafka"),
            other_feedback,
        ),
        blank=True,
        null=True,
        max_length=127
    )
