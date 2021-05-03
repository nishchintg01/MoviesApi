from django.db import models
from django.contrib.auth.models import User


class Collections(models.Model):
    uuid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=False, on_delete = models.CASCADE)
    Title = models.CharField(max_length=2000)
    Description = models.TextField()
    Movies = models.TextField()