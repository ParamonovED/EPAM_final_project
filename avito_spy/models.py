from django.db import models


class Target(models.Model):
    title = models.CharField(max_length=200)
    wanted_price = models.FloatField()

    def __str__(self):
        return self.title

