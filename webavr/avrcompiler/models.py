from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AssemblyProgram(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    code = models.TextField('AVR Code')
    modified = models.DateField('Last Modified')
    user = models.ForeignKey(User)
    def __str__(self):
        return self.name
