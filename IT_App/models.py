from django.db import models
from django.contrib.auth.models import User,AbstractUser
import random
import string

# Create your models here.
class CustomUser(AbstractUser):
    user_type = models.CharField(default=1, max_length=50)
    status = models.CharField(default=0,max_length=50) 
    Epwd = models.CharField(default=0,max_length=50) 
    TL = models.CharField(default=0,max_length=50)
    def generate_random_string():
        length=6
        characters=string.ascii_letters + string.digits
        random_string=''.join(random.choice(characters) for i in range(length))
        return random_string
class teamlead(models.Model):
    tl=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)


class Usermember(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    team = models.ForeignKey(teamlead,on_delete=models.CASCADE,null=True)

    assign= models.CharField(max_length=50) 
    address = models.CharField( max_length=255,null=True)
    number = models.CharField( max_length=255,null=True)
    course = models.CharField( max_length=255,null=True)
    file = models.FileField(upload_to='uploads/')
    department = models.CharField( max_length=255,null=True)
    

    
    

    
class project(models.Model):
    u_member=models.ForeignKey(Usermember,on_delete=models.CASCADE,null=True)
    c_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    topic=models.CharField( max_length=255,null=True)
    desc=models.CharField( max_length=255,null=True)
    requirement=models.CharField( max_length=255,null=True)
    modules=models.CharField( max_length=255,null=True)
    file=models.FileField(upload_to='uploads/')
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    crossed_date=models.CharField( max_length=255,null=True)
    cl_name =models.CharField( max_length=255,null=True)
    cl_address=models.CharField( max_length=255,null=True)
    cl_contact =models.CharField( max_length=255,null=True)
    cl_email =models.EmailField( max_length=255,null=True)


class project_TL(models.Model):
    project_name=models.ForeignKey(project,on_delete=models.CASCADE,null=True)
    team_lead=models.ForeignKey(Usermember,on_delete=models.CASCADE,null=True)
    newcount =models.IntegerField(null=True)


class module(models.Model):
    team=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    pro=models.ForeignKey(project_TL,on_delete=models.CASCADE,null=True)
    module_name =models.CharField( max_length=255,null=True)
    desc=models.CharField( max_length=255,null=True)
    requirement =models.CharField( max_length=255,null=True)
    file=models.FileField(upload_to='uploads/')
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    crossed_date=models.CharField( max_length=255,null=True)
    
class module_dev(models.Model):
    modu=models.ForeignKey(module,on_delete=models.CASCADE,null=True)
    dev=models.ForeignKey(Usermember,on_delete=models.CASCADE,null=True)
    mod_count=models.IntegerField(null=True)
class P_progress(models.Model):
    p_tl=models.ForeignKey(project_TL,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    file=models.FileField(upload_to='uploads/')
class m_progress(models.Model):
    m_dev=models.ForeignKey(module_dev,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    file=models.FileField(upload_to='uploads/')





