from django.db import models
from core import models as core_models

#### conversations 모델의 역할이 뭔지 새삼 재정립 필요.

# 대화방에 여러 user들이 존재하고, 각 user는 여러 대화방을 가질 수 있음.
class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        return str(self.created)

# 특정 대화방에서 특정 사용자가 말한 message를 표시함.
# Conversation 테이블을 상속받지 않는걸 보니,
# 대화방 별로 메세지 내용을 관리하는 것이 아니라, 사이트 내 모든 주고받은 메세지들이 Message 테이블에서 관리하는듯?
class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} says: {self.text}"