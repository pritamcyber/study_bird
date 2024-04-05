from django.db import models
from django.contrib.auth.models  import User
from django.db.models.deletion import CASCADE

# python manage.py sqlmigrate polls 0001 
# this is the command after that to see real sql query

# python manage.py shell
# after that you can play with sell to run modals 

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name
class Room(models.Model):
    participants =  models.ManyToManyField(User,related_name='participants',blank=True)
    
    # host
    host =  models.ForeignKey(User,on_delete=models.SET_NULL,null = True)
    topic  = models.ForeignKey(Topic,on_delete = models.SET_NULL,null = True)
    
    

    name = models.CharField(max_length=200)
    description =  models.TextField(null= True,blank =True)

#    participants 
    updated = models.DateTimeField(auto_now = True)
    created =  models.DateTimeField(auto_now_add = True)


    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Rooms'
        verbose_name_plural = 'ModelNames'
        ordering     = ['-updated','created']
    def __str__(self):
        return f"{self.name},{self.description}"
        

class Messages(models.Model):
    user = models.ForeignKey(User,on_delete = models.SET_NULL,null = True)

    room = models.ForeignKey(Room,on_delete = models.CASCADE)
    body = models.TextField() 
    # participent  
    updated =  models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = ''
        managed = True
        
        verbose_name_plural = 'ModelNames'
        ordering     = ['-updated','-created']
    
    def __str__(self):
        return self.body[0:50]