from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import User
from django_resized import ResizedImageField
# Create your models here.

class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.SmallIntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    edu = models.CharField(max_length=2)
    std = models.CharField(max_length=20)
    cpenumber = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    #count = models.CharField(max_length=2)
    count = models.BooleanField(default=False)
    profile_pic = ResizedImageField(size=[700, 700], crop=['middle', 'center'],null=False,blank=False,quality=100)
    profile_bg_pic = ResizedImageField(size=[400, 500], crop=['middle', 'center'],null=False, blank=False,quality=100)
    displayname = models.CharField(max_length=20,default='noverify')
    def __str__(self):
        return self.user.username

class OderCommand(models.Model):
    idcpesend = models.IntegerField(max_length=11)
    status = models.BooleanField(default=False)
    idcpeto = models.IntegerField(max_length=11)
    date = models.DateTimeField(auto_now_add=True)
    userid = ('id',)
    
    class Meta :
        db_table = 'odercommand'
        ordering =('-date',)
        verbose_name = 'รายการที่'
        verbose_name_plural = 'รายการ'

        def __str__(self):
            return self.user.username


class OderItem(models.Model):
    oder = models.ForeignKey(OderCommand,on_delete=models.CASCADE)

    class Meta:
        db_table = 'oderitem'
        verbose_name = 'รายการที่'
        verbose_name_plural = 'รายการ'

    def __str__(self):
        return self.oder
class Like(models.Model):
    idmy = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    id_someone = models.IntegerField(max_length=3)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Like'
        verbose_name = 'Links: '
        verbose_name_plural = 'Like-ecosystem'

class indexpic(models.Model):
    pic1 = models.ImageField()
    pic2 = models.ImageField()
    pic3 = models.ImageField()
    


