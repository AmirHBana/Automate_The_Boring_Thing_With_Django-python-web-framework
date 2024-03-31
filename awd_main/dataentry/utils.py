import hashlib
import os
import time

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
from emails.models import Email, Sent, EmailTracking, Subscriber

from bs4 import BeautifulSoup


def get_all_custom_models():

    default_models = ['ContentType', 'Session', 'LogEntry', 'Permission', 'Group', 'User', 'Upload']

    # Try to get all the apps

    custom_models = []

    for model in apps.get_models():

        if model.__name__ not in default_models:

            custom_models.append(model.__name__)

    return custom_models


def check_csv_errors(file_path, model_name):

    # Search for the model across all installed apps

    model = None

    for app_config in apps.get_app_configs():

        # Try to search for the model

        try:

            model = apps.get_model(app_config.label, model_name)

            break  # stop searching once the model found

        except LookupError:

            continue  # model not found in this app continue searching the other model

    if not model:

        raise CommandError(f'Model {model_name} not found in any apps!')


    # compare csv header with model's field names
    # get all the field names of the model that we found
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
    print(model_fields)

    try:
        with open(file_path, 'r') as file:

            reader = csv.DictReader(file)

            csv_header = reader.fieldnames

            # compare csv header with model's field names

            if csv_header != model_fields:

                raise DataError(f'CSV file does not match {model_name} Table fields. ')

    except Exception as e:

        raise e

    return model


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):

    try:

        from_email = settings.DEFAULT_FROM_EMAIL

        for recipient_email in to_email:

            # Create Email tracking record

            new_message = message

            if email_id:

                email = Email.objects.get(pk=email_id)

                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)

                timestamp = str(time.time())

                data_to_hash = f"{recipient_email}{timestamp}"

                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()

                email_tracking = EmailTracking.objects.create(
                    email=email,
                    subscriber=subscriber,
                    unique_id=unique_id,
                )

                # Generate the tracking pixel

                # TODO : this line blow should be a domain server name and http://127.0.0.1:8000 it's gonna work on localhost only you can use ngrok for host

                click_tracking_url = f"http://127.0.0.1:8000/emails/track/click/{unique_id}"

                open_tracking_url = f"http://127.0.0.1:8000/emails/track/open/{unique_id}"

                # Search for the links in the email body

                soup = BeautifulSoup(message, 'html.parser')

                urls = [a['href'] for a in soup.find_all('a', href=True)]

                print('urls ==>>>', urls)

                # If there are links or urls in the body email , inject our click tracking url to that link

                if urls:

                    for url in urls:

                        # make the final tracking url

                        tracking_url = f"{click_tracking_url}?url={url}"

                        new_message = new_message.replace(f"{url}", f"{tracking_url}")

                else:

                    print("no URL's found in the email content")

                # create email content with tracking pixel image

                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>"

                new_message += open_tracking_img

            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])

            if attachment is not None:

                mail.attach_file(attachment)

            mail.content_subtype = "html"

            mail.send()

        # Store the total sent emails inside the Sent model
        if email_id:

            sent = Sent()

            sent.email = email

            sent.total_sent = email.email_list.count_emails()

            sent.save()

    except Exception as e:

        raise e


def generate_csv_file(model_name):

    # Generate the timestamp of current date and time

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # define the csv file name/path

    export_dir = 'exported_data'

    file_name = f'exported_{model_name}_data_{timestamp}.csv'

    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)

    print("file path ===>>> ",file_path)

    return file_path