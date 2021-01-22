from django.db import models


class Target(models.Model):
    title = models.CharField(max_length=200)
    wanted_price = models.FloatField()
    active_ads = models.IntegerField(null=True)
    average_price = models.FloatField(null=True)
    dynamic = models.FloatField(null=True)
    price_difference = models.FloatField(null=True)

    def __str__(self):
        return self.title


class Ad(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    price = models.CharField(max_length=20)

    def __str__(self):
        return self.title
