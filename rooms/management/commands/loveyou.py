from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "This command tells me that he loves me"


    # parser 는 또 뭐하는애임?
    def add_arguments(self, parser):
        return super().add_arguments("--times", help="How many times do you want me to tell you that I love you?")

    # options는 어디서 받아오는 kwargs입력받은애랑 무슨 관계?
    def handle(self, *args, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            self.stdout.write(self.style.SUCCESS("I lov you"))
