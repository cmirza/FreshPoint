from django.db import models


class Vegetable(models.Model):
    veg_name = models.CharField(max_length=50)
    veg_type = models.CharField(max_length=50)
    veg_image = models.CharField(max_length=25)
    veg_desc = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Vegetable'
        verbose_name_plural = 'Vegetables'

    def __str__(self):
        return f'{self.veg_name}'


class State(models.Model):
    state_name = models.CharField(max_length=2)
    state_full = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return f'{self.state_name}'


class Season(models.Model):
    seasons = models.CharField(max_length=100)
    seasons_veg = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    seasons_state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'

    def __str__(self):
        return f'{self.seasons_veg} - {self.seasons_state}'
