from awd_main.celery import app
import time
from django.core.management import call_command
from dataentry.utils import send_email_notification, generate_csv_file
from django.conf import settings


@app.task
def celery_test_task():

    time.sleep(5)   # Simulation of any task's going to take 10 seconds

    # Send an email when task done

    mail_subject = 'Test Subject'

    message = 'This is a test email message.'

    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject, message, to_email)

    return 'Email Send successfully.'


@app.task
def import_data_task(file_path, model_name):

    try:

        call_command('importdata', file_path, model_name)

    except Exception as e:

        raise e

    # Send the user a notification by email

    mail_subject = 'Import data Completed.'

    message = 'Your data has been Imported successfully.'

    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject, message, [to_email])

    return 'Data Imported successfully.'


@app.task
def export_data_task(model_name):

    try:

        call_command('exportdata', model_name)

    except Exception as e:

        raise e

    file_path = generate_csv_file(model_name)



    # Send the Email with the attachment

    mail_subject = 'Export data Completed successfully. '

    message = 'Your data has been Emported successfully. please find the attachment'

    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject, message, [to_email], attachment=file_path)

    return 'Export Data task executed successfully.'