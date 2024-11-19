from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.title}'
