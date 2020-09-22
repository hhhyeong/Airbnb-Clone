import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


# Room 모델의 objects 만들기.
# python manage.py seed_rooms
class Command(BaseCommand):

    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # Room object를 만들기 위해, host, room_type필드에 각각 Users, RoomType모델의 값이 필요하다.
        # => 랜덤하게 저장될 수 있도록 함.
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        # print(room_types)
        seeder.add_entity(
            room_models.Room,
            number,
            {
                # name 필드에 왜 faker.address()값이 들어가지??
                "name": lambda x: seeder.faker.address(),
                # host 필드에 all_users의 값들 중 random으로 설정.
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                # 수용가능한 손님 수는 랜덤한 숫자 값으로 설정.
                # "guests": lambda x: random.randint(1, 20),
                # "price": lambda x: random.randint(1, 300),
                # "beds": lambda x: random.randint(1, 5),
                # "bedrooms": lambda x: random.randint(1, 5),
                # "baths": lambda x: random.randint(1, 5),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
