from django.core.management.base import BaseCommand

from dataentry.models import Student


# i want to add some date to the database using custom command

class Command(BaseCommand):

    help = 'InsertIt will insert date to the database'

    def handle(self, *args, **kwargs):

        # write the logic here

        # add 1 data

        dataset = [

            {'roll_no': 1002, 'name': 'Mohammad', 'age': 21},
            {'roll_no': 1003, 'name': 'John', 'age': 22},
            {'roll_no': 1004, 'name': 'Mike', 'age': 23},
            {'roll_no': 1005, 'name': 'Joseph', 'age': 23},
            {'roll_no': 1006, 'name': 'Mikel', 'age': 26},

        ]

        for data in dataset:

            roll_no = data['roll_no']

            existing_record = Student.objects.filter(roll_no=roll_no).exists()

            if not existing_record:

                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])

            else:
                self.stdout.write(self.style.WARNING(f'Student with roll number {roll_no} already exists.'))

        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))