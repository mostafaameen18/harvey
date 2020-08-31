from django.db import models

class csvFile(models.Model):
    file = models.FileField()

    def __str__(self):
        return str(self.file)