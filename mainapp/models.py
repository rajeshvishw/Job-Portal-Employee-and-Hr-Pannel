from django.db import models

class masterModel(models.Model):
    email = models.EmailField()
    pasword = models.CharField(max_length=10)
    otp = models.CharField(max_length=10)
    role = models.CharField(max_length=20)

class userModel(models.Model):
    mastermodel = models.ForeignKey(masterModel,on_delete = models.CASCADE)
    firstname = models.CharField(max_length=20,blank=True,null=True)
    lastname = models.CharField(max_length=20,blank=True,null=True)
    mobile = models.CharField(max_length=13,null=True,blank=True)
    city = models.CharField(max_length=20,blank=True,null=True)
    state = models.CharField(max_length=20,blank=True,null=True)
    candidatelogo = models.FileField(upload_to="candidatelogo/",blank=True,null=True)
    
class companyModel(models.Model):
    mastermodel = models.ForeignKey(masterModel,on_delete = models.CASCADE)
    firstname = models.CharField(max_length=20,blank=True,null=True)
    lastname = models.CharField(max_length=20,blank=True,null=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    city = models.CharField(max_length=20,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    companylogo = models.FileField(upload_to="company/",blank=True,null=True)

class postjobModel(models.Model):
    companyname = models.CharField(max_length=40,null=True,blank=True)
    companyid = models.ForeignKey(companyModel,on_delete=models.CASCADE)
    jobtitle = models.CharField(max_length=40,null=True,blank=True)
    jobdescription = models.TextField()
    city = models.CharField(max_length=20,null=True,blank=True)
    state = models.CharField(max_length=20,null=True,blank=True)
    salary = models.CharField(max_length=20,null=True,blank=True)
    salary_choose=[
        ('month','month'),
        ('year','year')
    ]
    salarytype = models.CharField(max_length=30,choices=salary_choose,blank=True,null=True)
    companyimage = models.FileField(upload_to="companyimage/",blank=True,null=True)