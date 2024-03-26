from django.core.management.base import BaseCommand

# create our custumize command like python manage.py runserver
# Proposed command = python manage.py greeting YourName
# Proposed output = Hi {name}, Good morning

class Command(BaseCommand):

    help = 'Greets the User'

    def add_arguments(self, parser):

        parser.add_argument('name', type=str, help='Specifies user name')

    def handle(self, *args, **kwargs):

        # write the logic

        name = kwargs['name']

        greeting = f'Hello {name}, Good Morning'
        self.stdout.write(self.style.SUCCESS(greeting))

        #stderr  for show errors in console
        #stdout  for show out put to console