import os
import shutil
import uuid
from datetime import datetime, timedelta
from hashlib import sha256
from pprint import pprint

import git
import requests
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.utils.text import slugify
from ipware import get_client_ip
from jinja2 import FileSystemLoader, Environment
from pytz import utc


def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def process_data(request, form_classes):
    # Get data from forms
    data = {}
    # Get data from single field forms
    single_fields = ['project_name', 'programming_language', 'generate_code_examples', 'nats', 'memcached',
                     'redis', 'prometheus', 'clickhouse', 'elasticsearch', 'mailhog']
    for field in single_fields:
        data[field] = form_classes[f"{field}_form"].cleaned_data[field]

    # Slug for project name
    data['slug'] = slugify(data['project_name'])

    # Git
    git_data = form_classes['git_form'].cleaned_data
    data['git_repo'] = git_data['repo']
    data['gitignore'] = git_data['gitignore']

    # Databases
    database_forms = ['mysql_form', 'postgres_form', 'mariadb_form', 'mongodb_form']
    for field in database_forms:
        if field in form_classes.keys():
            db_data = form_classes[field].cleaned_data
            if db_data['active']:
                db_name = field.removesuffix('_form')
                data[db_name] = dict(
                    database_name=db_data['database_name'],
                    username=db_data['username'],
                    password=db_data['password'],
                    port=db_data['port']
                )
                if db_data.get("phpmyadmin"):
                    data[db_name]['phpmyadmin'] = db_data['phpmyadmin']
                if db_data.get("mongo_express"):
                    data[db_name]['mongo_express'] = db_data['mongo_express']
                if db_data.get("pgadmin"):
                    data[db_name]['pgadmin'] = db_data['pgadmin']

    # Message queuing
    rabbitmq_data = form_classes['rabbitmq_form'].cleaned_data
    if rabbitmq_data['active']:
        data['rabbitmq'] = dict(
            username=rabbitmq_data['username'],
            password=rabbitmq_data['password'],
            management=rabbitmq_data['management']
        )

    # Metrics
    graylog_data = form_classes['graylog_form'].cleaned_data
    if graylog_data['active']:
        data['graylog'] = dict(
            password_secret=graylog_data['password_secret'],
            hashed_password=graylog_data['hashed_password']
        )

    grafana_data = form_classes['grafana_form'].cleaned_data
    if grafana_data['active']:
        data['grafana'] = dict(
            username=grafana_data['username'],
            password=grafana_data['password'],
        )

    # Create project folder
    user_path = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4()))
    os.mkdir(user_path)
    project_path_root = os.path.join(user_path, data['slug'])
    os.mkdir(project_path_root)
    project_path = os.path.join(project_path_root, data['slug'])
    os.mkdir(project_path)

    if data['gitignore']:
        create_gitignore(project_path_root, data.get('programming_language', ""))
    if data['git_repo']:
        initialize_git_repo(project_path_root)

    # Create template files
    create_file_from_template(project_path_root, data, "Readme.md")
    create_file_from_template(project_path_root, data, "docker-compose.yml")
    create_file_from_template(project_path, data, "Dockerfile")

    # Create programming language specific templates
    if data['programming_language'] == "python":
        initialize_programming_language(
            data=data,
            project_path=project_path,
            subdirectory="python",
            main_script="main.py",
            libraries_file="requirements.txt",
            examples=['mariadb', 'memcached', 'mongodb', 'mysql', 'nats', 'postgres', 'redis', 'rabbitmq_send',
                      'rabbitmq_receive'],
            extension="py"
        )
    elif data['programming_language'] == "node":
        initialize_programming_language(
            data=data,
            project_path=project_path,
            subdirectory="node",
            main_script="index.js",
            libraries_file="package.json",
            examples=['mariadb', 'memcached', 'mongodb', 'mysql', 'nats', 'postgres', 'redis', 'rabbitmq_send',
                      'rabbitmq_receive'],
            extension="js"
        )

    remove_empty_lines(os.path.join(project_path_root, "docker-compose.yml"))

    # Create zip archive
    zip_name = f"{data['slug']}-scaffoldy"
    shutil.make_archive(os.path.join(user_path, zip_name), 'zip', user_path, data['slug'])

    # Serve as download
    print('Downloading ' + data['project_name'])
    response = download(os.path.join(user_path, f"{zip_name}.zip"))

    # Remove folder
    shutil.rmtree(path=user_path)

    data['session_id'] = get_session_id(request)
    client_ip, is_routable = get_client_ip(request)
    if client_ip is not None and is_routable:
        hashed_ip = sha256(client_ip.encode('utf-8')).hexdigest()
        data['ip_address'] = hashed_ip

    # return response
    return response

def initialize_programming_language(data, project_path, subdirectory, main_script, libraries_file, examples, extension):
    # Create main script
    create_file_from_template(project_path, data, main_script, subdirectory=subdirectory)
    # Create libraries file
    create_file_from_template(project_path, data, libraries_file,
                              subdirectory=subdirectory)
    remove_empty_lines(os.path.join(project_path, libraries_file))

    # Create code examples
    if data['generate_code_examples']:
        if any(data.get(service) for service in examples):
            code_examples_path = os.path.join(project_path, "code_examples")
            os.mkdir(code_examples_path)
            for example in examples:
                # Check if service of example name is included
                service = example.split('_')[0]
                if data.get(service):
                    create_file_from_template(code_examples_path, data, f"{example}_example.{extension}",
                                              subdirectory=f"{subdirectory}/code_examples")


def download(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline;filename=' + os.path.basename(path)
            return response

    raise Http404


def create_text_file(path, name, content):
    with open(os.path.join(path, name), "w") as file:
        file.write(content)


def create_gitignore(path, options):
    # Create .gitignore from gitignore.io
    options += ",jetbrains,visualstudio,eclipse"
    gitignore_content = requests.get(f"https://www.toptal.com/developers/gitignore/api/{options}").text
    create_text_file(path, ".gitignore", gitignore_content)


def initialize_git_repo(path):
    repo = git.Repo.init(path)
    repo.git.add(all=True)
    repo.index.commit("initial commit")


def create_file_from_template(path, data, template_name, subdirectory=""):
    # Initialize jinja2
    file_loader = FileSystemLoader(
        os.path.join(settings.SITE_ROOT,
                     f'generator/templates/{subdirectory}'))
    env = Environment(loader=file_loader)

    template = env.get_template(f'{template_name}.jinja2')

    content = template.render(**data)
    create_text_file(path, template_name, content)


def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename) as in_file, open(filename, 'r+') as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()
