from django.db import models
from django.contrib.auth.models import User

class csvFile(models.Model):
    file = models.FileField()

    def __str__(self):
        return str(self.file)


class reset_code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return str(self.user.username)