from django.db import models
from django.db.models import Avg, Sum


# Create your models here.


class Module(models.Model):
    m_id = models.AutoField(primary_key=True, unique=True)
    m_code = models.CharField(max_length=64)
    m_name = models.CharField(max_length=256)
    ac_year = models.PositiveIntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return '%s %s %s %s %s'%(self.m_id, self.m_code, self.m_name, self.ac_year, self.semester)


class Professor(models.Model):
    p_id = models.AutoField(primary_key=True, unique=True)
    p_code = models.CharField(max_length=64)
    p_name = models.CharField(max_length=128)
    m_id = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s'%(self.p_id, self.p_code, self.p_name, self.m_id)


class Rate(models.Model):
    r_id = models.AutoField(primary_key=True, unique=True)
    m_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    p_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return '%s %s %s %s'%(self.r_id, self.m_id, self.p_id, self.rate)


class User(models.Model):
    u_id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=32)
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=64)


