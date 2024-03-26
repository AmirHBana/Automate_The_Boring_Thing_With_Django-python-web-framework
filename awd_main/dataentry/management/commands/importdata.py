import csv

from django.core.management.base import BaseCommand, CommandError

from django.apps import apps
# from dataentry.models import Student
# kaggle site for the Dataset

# Proposed command = python manage.py importdata file_path model_name
# run this command   *** python manage.py importdata /YOUR_SYSTEM_PATH/awd_main/Datasets/Datasets/student_data.csv student***

class Command(BaseCommand):

    help = 'Import data from CSV file'

    def add_arguments(self, parser):

        parser.add_argument('file_path', type=str, help='CSV file path')

        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):

        #logic goes here

        file_path = kwargs['file_path']

        model_name = kwargs['model_name'].capitalize()

        # Search for the model across all installed apps
        model = None
        for app_config in apps.get_app_configs():

            # Try to search for the model

            try:

                model = apps.get_model(app_config.label, model_name)

                break # stop searching once the model found

            except LookupError:

                continue # model not found in this app continue searching the other model

        if not model:

            raise CommandError(f'Model {model_name} not found in any apps!')

        with open(file_path, 'r') as file:

            reader = csv.DictReader(file)

            for row in reader:

                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully'))
