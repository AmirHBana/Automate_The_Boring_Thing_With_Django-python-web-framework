import csv

from django.core.management.base import BaseCommand, CommandError

from dataentry.utils import check_csv_errors
from django.apps import apps
from django.db import DataError


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

        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:

            reader = csv.DictReader(file)

            for row in reader:

                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully'))
