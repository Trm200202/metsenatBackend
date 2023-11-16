from django.db import models
import re
from django.core.validators import RegexValidator
from django import forms
from django.http import HttpResponse
import requests
# Create your models here.

class Sponsor(models.Model):

    class StatusChoice(models.TextChoices):
        MODERATION = "Moderation","Moderatsiya"
        NEW = "New", "Yangi"
        APPROVED = "Approved", "Tasdiqlangan"
        CANCELLED = "Cancelled", "Bekor qilingan"


    class TypeChoice(models.TextChoices):
        LEGAL = "legal", "yuridik"
        PHYSICAL = "physical", "jismoniy"
        


    class TransactionType(models.TextChoices):
        CASH = "cash", "naqd"
        CARD = "card", "karta"

    

    full_name = models.CharField(max_length=100, verbose_name="To'liq ism")
    organization_name = models.CharField(max_length=100, verbose_name="Tashkilot nomi",
                                          null=True,
                                          blank=True)
    phone_number = models.CharField(max_length=50,
                                     validators=[RegexValidator(r'^\+998\d{9}$')],
                                     verbose_name="Telefon raqami")
    amount = models.PositiveIntegerField(verbose_name="Homiylik summasi")
    created_at = models.DateField(auto_now_add=True, verbose_name="Ariza sanasi")
    status = models.CharField(max_length=50,
                               choices=StatusChoice.choices,
                               default=StatusChoice.NEW,
                               verbose_name="Homiy holati")
    type = models.CharField(max_length=50, 
                            choices=TypeChoice.choices,
                            verbose_name="Shaxs turi")
    
    transaction_type = models.CharField(max_length=50,
                                         verbose_name="To'lov turi",
                                         choices=TransactionType.choices,
                                         default=TransactionType.CARD)
    
    
    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
    





class University(models.Model):
    name = models.CharField(max_length=200, verbose_name="Universitet nomi")


    def __str__(self):
        return self.name
phone_number = models.CharField(max_length=50,
                                     validators=[RegexValidator(r'^\+998\d{9}$')],
                                     verbose_name="Telefon raqami")
class Student(models.Model):
     
    class DegreeChoice(models.TextChoices):
        BACHELOR = "bachelor", "bakalavr"
        MASTER = "master", "magistor"

    phone_number = models.CharField(max_length=50,
                                     validators=[RegexValidator(r'^\+998\d{9}$')],
                                     verbose_name="Telefon raqami",)
    full_name = models.CharField(max_length=100, verbose_name="To'liq ism")
    contract = models.PositiveIntegerField(verbose_name="kantrakt summasi")
    degree = models.CharField(max_length=50,
                              choices=DegreeChoice.choices,
                              default=DegreeChoice.BACHELOR,
                              verbose_name="Darajasi")
    university = models.ForeignKey(University, on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)


    def __str__(self):
        return self.full_name




class StudentSponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT,
                                verbose_name="Sponsor", 
                                related_name="student_sponsors")
    student = models.ForeignKey(Student, on_delete=models.PROTECT,
                                verbose_name="Student",
                                related_name="student_sponsors")
    amount = models.PositiveIntegerField(verbose_name="Ajratilgan summa")

    def __str__(self):
        return f"{self.sponsor} - {self.student}"



