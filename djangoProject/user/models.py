from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Userinfo(AbstractUser):
    """
    用户信息表
    """
    money = models.IntegerField(verbose_name='资金', default=2000)
    nickname = models.CharField(verbose_name='昵称', max_length=32, default='')
    title = models.CharField(verbose_name='称号', max_length=32, default='一贫如洗')
