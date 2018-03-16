from django.db import models

# Create your models here.
class stclass(models.Model):
    classname = models.CharField(max_length=10)
    
    def __str__(self):
        return self.classname

class studentid(models.Model):
    sclass=models.ForeignKey(stclass, on_delete=models.CASCADE, null=True)
    userid=models.IntegerField(null=True, blank=True)
    
class student_detail(models.Model):
    userid=models.IntegerField()
    firstname=models.CharField(max_length=200)
    fieldid=models.IntegerField()
    data=models.CharField(max_length=200)
    
class student_marks(models.Model):
    userid=models.IntegerField()
    firstname=models.CharField(max_length=200)
    Class=models.CharField(max_length=50)
    coursename=models.CharField(max_length=100)
    gradebookitem=models.CharField(max_length=100,null=True, blank=True)
    grade=models.IntegerField()
    substring=models.CharField(max_length=1000,null=True, blank=True)
    raw_grade=models.IntegerField(blank=True, null=True)

class student_marks12(models.Model):
    userid=models.IntegerField(null=True, blank=True)
    subject=models.CharField(max_length=100,null=True, blank=True)
    description=models.CharField(max_length=500,null=True, blank=True)
    term=models.CharField(max_length=500,null=True, blank=True)
    grade=models.CharField(max_length=500,null=True, blank=True)
    remark=models.CharField(max_length=1000,null=True, blank=True)
    modified=models.IntegerField(null=True, blank=True)

class nalanda(models.Model):
    userid=models.IntegerField(null=True, blank=True)
    subject=models.CharField(max_length=100,null=True, blank=True)
    gradebookitem=models.CharField(max_length=100,null=True, blank=True)
    grade=models.CharField(max_length=500,null=True, blank=True)
    modified=models.IntegerField(null=True, blank=True)
    substring=models.CharField(max_length=1000,null=True, blank=True)