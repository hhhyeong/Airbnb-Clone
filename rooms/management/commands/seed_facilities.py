from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import Facility


# Amenity 모델의 objects 만들기.
# python manage.py seed_facilities
class Command(BaseCommand):

    help = "This command creates facilities"

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("Facilities created!"))
