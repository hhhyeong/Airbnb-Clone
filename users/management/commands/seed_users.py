from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


# Amenity 모델의 objects 만들기.
# python manage.py seed_users

# AbstractUser클래스에 is_staff, is_superuser 값이 있음.
class Command(BaseCommand):

    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many users do you want to create"
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        number = options.get("number", "1")
        seeder = Seed.seeder()
        # Users모델에서 기본 제공하는 권한 중 staff, superuser의 권한을 가질 경우,
        # admin패널을 볼 수 있음. => 두 권한을 모두 갖지 않는 users객체를 만들거임.
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
