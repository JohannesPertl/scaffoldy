from django import forms
from django.utils.safestring import mark_safe

from .base_forms import FoldoutForm


class DatabaseForm(FoldoutForm):
    database_name = forms.CharField(label="Database name", required=False)
    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(label="Password", help_text=mark_safe("This password is not saved and will only be used for generating the docker-compose.yml file. <br> For security reasons, you should change it in production"), required=False)
    port = forms.IntegerField(label="Port", required=False)

    required_fields = ['database_name', 'username', 'password', 'port']
    initial_port = None
    help_text = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial_port:
            self.fields['port'].initial = self.initial_port


class MySQLForm(DatabaseForm):
    phpmyadmin = forms.BooleanField(
        label="Include phpMyAdmin",
        help_text="phpMyAdmin is web administration tool for MySQL and MariaDB",
        required=False
    )
    label = "MySQL"
    prefix = 'mysql'
    help_text = 'MySQL is an open-source relational database management system'
    initial_port = 3304


class MariaDBForm(DatabaseForm):
    phpmyadmin = forms.BooleanField(
        label="Include phpMyAdmin",
        help_text="phpMyAdmin is web administration tool for MySQL and MariaDB",
        required=False
    )
    label = "MariaDB"
    prefix = 'mariadb'
    help_text = 'MariaDB is a community-developed, commercially supported fork of MySQL'
    initial_port = 3306


class PostgreSQLForm(DatabaseForm):
    pgadmin = forms.BooleanField(
        label="Include pgAdmin",
        help_text="pgAdmin is a web administration tool for PostgreSQL",
        required=False
    )
    label = "PostgreSQL"
    prefix = 'postgres'
    help_text = 'PostgreSQL, also known as Postgres, is an open-source relational database management system emphasizing extensibility and SQL compliance'
    initial_port = 5432


class MongoDBForm(DatabaseForm):
    mongo_express = forms.BooleanField(
        label="Include Mongo Express",
        help_text="Mongo Express is a web-based administrative interface for MongoDB",
        required=False
    )
    label = "MongoDB"
    prefix = 'mongodb'
    help_text = 'MongoDB is a source-available cross-platform document-oriented NoSQL database program'
    initial_port = 27017
