from django.db import models
from django.contrib.auth.models import AbstractUser

from .choices import *


class User(AbstractUser):
    email = models.EmailField(null=True, default=None)

    USER_TYPE = (
        ('st', 'Студент'),
        ('com', 'Компания'),
        ('unv', 'Университет')
    )

    user_type = models.CharField(choices=USER_TYPE, max_length=80)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    foundation_year = models.IntegerField(null=True, default=0)
    description = models.TextField(null=True, default=None)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.name)


class SubjectArea(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % (self.title)


class Competency(models.Model):
    title = models.CharField(max_length=150)
    subject_area = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.title)


class StudentCompetency(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    who_verified = models.ManyToManyField(User, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'competency',)


class University(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    foundation_year = models.IntegerField()
    description = models.TextField(null=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    verified = models.BooleanField(default=False)
    bg_src = models.CharField(max_length=200, null=True, blank=True, default='http://2bddea4c.ngrok.io/static/img/no-image.jpg')
    icon_src = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.title)


class UniversityProgram(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    degree = models.CharField(choices=DEGREE, default=None, max_length=3)
    competencies = models.ManyToManyField(Competency, null=True, default=None)

    def __str__(self):
        return '%s' % (self.title)


class StudentEducation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    degree = models.CharField(choices=DEGREE, default=None, max_length=3)
    program = models.ForeignKey(UniversityProgram, on_delete=models.CASCADE)
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    verified = models.BooleanField(default=False)


class StudentJob(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    position = models.CharField(max_length=60)
    verified = models.BooleanField(default=False)


class SubjectAreaVacancies(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % (self.title)


class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.TextField(null=True)
    competencies = models.ManyToManyField(Competency, null=True, default=None)
    subject_area = models.ForeignKey(SubjectAreaVacancies, on_delete=models.CASCADE, null=True, default=None)
