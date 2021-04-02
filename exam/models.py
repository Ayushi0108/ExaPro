from django.db import models

# Create your models here.

class CreateExam(models.Model):
    eid = models.CharField(max_length=20,primary_key=True)
    email = models.EmailField()
    exam_name = models.CharField(max_length=50)
    subject = models.TextField(max_length=50)
    duration = models.IntegerField()
    tmarks = models.IntegerField()
    status = models.BooleanField(default=False)

class Eligibility(models.Model):
    eid = models.CharField(max_length=20,primary_key=True)
    all_emails = models.TextField()
    
class SetQPaper(models.Model):
    id = models.AutoField(primary_key=True)
    eid = models.CharField(max_length=20,null=False)
    questions = models.CharField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    corr_ans = models.CharField(max_length=100)
    marks = models.IntegerField()
