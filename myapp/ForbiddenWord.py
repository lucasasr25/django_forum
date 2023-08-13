from django.db import models

class ForbiddenWord(models.Model):
    word = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.word
