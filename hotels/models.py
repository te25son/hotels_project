from django.db import models


class City(models.Model):
    """
    Keeps a single city reference that will then
    be used in relation with :model: `hotels.Hotel`.
    """
    abbrv = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'cities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Hotel(models.Model):
    """
    Keeps a single hotel reference related to
    :model: `hotels.City`.
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    loc = models.CharField(max_length=100)
    name = models.CharField(max_length=250)

    class Meta:
        unique_together = ('loc', 'name')
        ordering = ['city__name', 'name']

    def __str__(self):
        return self.name
