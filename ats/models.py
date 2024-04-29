from django.db import models

# Create your models here.from django.db import models
class keyword(models.Model):
    word = models.CharField(max_length=50, unique=True)

class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    keywords = models.ManyToManyField(keyword, blank=True)
    exp = models.DecimalField(max_digits = 4,decimal_places = 2, blank=True)
    cgpa = models.DecimalField(max_digits= 5,decimal_places=2, null=True)
    resume = models.FileField(upload_to='resumes/', null=True,blank=True)
    jd=models.IntegerField(null=True)

    def __str__(self):
        return self.name


