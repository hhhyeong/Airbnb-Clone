from django.db import models
from core import models as core_models

# 방에 대한 문의, 후기 기능.
# guest와 그 외의 다른 user들이 host에게 문의할 수 있음.

# related_name : FK, MTM 필드의 속성.
#    -
class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    # def __str__(self):
    #     # return str(self.created)
    #     # 참가자들 리스트
    #     usernames = []
    #     for user in self.participants.all():
    #         usernames.append(user.username)
    #     return ", ".join(usernames)

    # # self의 정체? 본인 Conversations 클래스는 messages필드를 가지고있지 않은데???
    # def count_messages(self):
    #     return self.messages.count()

    # count_messages.short_description = "Number of Messages"

    # def count_participants(self):
    #     return self.participants.count()

    # count_participants.short_description = "Number of Participants"


# 특정 대화방에서 특정 사용자가 말한 message를 표시함.
# Conversation 테이블을 상속받지 않는걸 보니,
# 대화방 별로 메세지 내용을 관리하는 것이 아니라, 사이트 내 모든 주고받은 메세지들이 Message 테이블에서 관리하는듯?
class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="message", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="message", on_delete=models.CASCADE
    )

    def __str__(self):
        # text는 어디서나온거????
        # return f"{self.user} says: {self.text}"
        return f"{self.user} says: {self.message}"