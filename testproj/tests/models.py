from django.db import models


class TestModel(models.Model):
    data = models.CharField(max_length=32, blank=True)
    count = models.IntegerField(default=0)


    def __str__(self):
        return str(self.pk)
