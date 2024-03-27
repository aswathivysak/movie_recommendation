from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    desc_text='Hey,there this is a deafult text description,You can change onafter clicking on "Edit" or going to your profile page.'
    desc=models.CharField(default=desc_text,max_length=200,null=True)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
