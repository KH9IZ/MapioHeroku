from django.db import models

# Create your models here.


class Square(models.Model):
    vertical_id = models.IntegerField(blank=False)
    horizontal_id = models.IntegerField(blank=False)
    owner = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    time_stamp = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.owner.user_id) + "_" + str(self.vertical_id) + "_" + str(self.horizontal_id)


class UserProfile(models.Model):
    color = models.CharField(max_length=15, blank=False)
    user_id = models.CharField(max_length=50, blank=False, primary_key=True)

    def get_user_score(self):
        return Square.objects.filter(owner=self).count()

    def __str__(self):
        return str(self.user_id) + "_" + str(self.color)
