from django.db import models

# Create your models here.
class Family(models.Model):
    name = models.CharField(max_length=32)
    photo = models.ImageField(null=True, upload_to='familyMember/', blank=True,
                              default='familyMember/wu.jpg')

    def __str__(self):
        return self.name


# class UserInfo(models.Model):
# #     username = models.CharField(max_length=32,unique=True)
# #     password = models.CharField(max_length=32)
# #     email = models.EmailField()