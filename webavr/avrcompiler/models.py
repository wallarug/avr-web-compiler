from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class AssemblyProgram(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    code = models.TextField('AVR Code')
    created = models.DateTimeField(editable=False)
    modified = models.DateField()
    user = models.ForeignKey(User)

    def create(self, name, code, user):
        #program = self.create(name=name,code=code,user=user)
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AssemblyProgram, self).create()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AssemblyProgram, self).save()

    def __str__(self):
        return self.name

    # Getter methods
    def getName(self):
        return self.name
    def getCode(self):
        return self.code
    def getId(self):
        return self.id
