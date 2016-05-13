from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
def file_name(instance, filename):
    return '/'.join([User.username, ''.join([instance.name, '.c'])])
    #return '/'.join([User.username, ''.join([instance.title, datetime.now().strftime('%m%d%Y-%Hh%Mm%Ss')])])

class CProgram(models.Model):
    name = models.CharField(max_length=128)
    code_file = models.FileField(upload_to=file_name, blank=True,
                                 help_text=('Allowed type - .c, .h'))
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    user = models.ForeignKey(User)
    def save(self, code=0, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        if code != 0:
            self.code = code
        return super(CProgram, self).save()

    def __str__(self):
        return self.name