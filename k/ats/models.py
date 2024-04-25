from django.db import models

class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    #keywords = models.TextField(blank=True)
    #overall_experience = models.CharField(max_length=100, blank=True)
    resume_file = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name
