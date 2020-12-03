import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
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
                # name필드에 너무 긴 문장이 들어가서 faker써서 주소 가라데이터를 넣음.
                # https://faker.readthedocs.io/en/master/
                "name": lambda x: seeder.faker.address(),
                # host 필드에 all_users의 값들 중 random으로 설정.
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                # 수용가능한 손님 수는 랜덤한 숫자 값으로 설정.(음수값 안나오도록)
                "guests": lambda x: random.randint(1, 20),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        # seeder.execute()
        created_photos = seeder.execute()
        # print(created_photos) => python manage.py seed_rooms명령어로 콘솔에 찍어보기.
        # 랜덤으로 만든 사진의 id값 구하기.
        created_clean = flatten(list(created_photos.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            # photo_seed디렉토리에 있는 파일을 자동으로 import 하기위해,
            # 1~31까지의 숫자를 랜덤으로 import할거임.
            # 만들 photos들의 개수를 랜덤으로 생성.
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    # fake sentence로 내용 채우기.
                    caption=seeder.faker.sentence(),
                    # FK(room)를 가진 Photo 모델 생성.
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            # amenities를 랜덤으로 저장하기.
            for a in amenities:
                # 모든 amenities들의 각 요소들에 대하여, 랜덤으로 숫자를 뽑아서, 짝수일 경우만 add()수행.
                # 거의 50%의 확률로 add()가 수행되겠지.
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    # MTM필드에서 무언가를 추가하는 방법. add()
                    room.amenities.add(a)
            # facilities 랜덤으로 저장하기.
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            # rules 랜덤으로 저장하기.
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    # "Room" objects has "house_rules" attribute.
                    room.house_rules.add(r)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))