from django.db import models


class AudioFile(models.Model):
    audio = models.FileField(upload_to='media/')


class Text(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content
