from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('provider', 'Provider')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='client')
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    

class Service(models.Model):
    
    name = models.CharField(max_length=255, default='Serivce')
    description = models.TextField(default='Short discription')
    duration = models.IntegerField(help_text="Duration in minutes")
    
    def __str__(self):
        return str(self.name)
    
class ProviderService(models.Model):
    provider = models.ForeignKey(Profile, limit_choices_to={'user_type' : 'provider'}, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("provider", "service")
        
    def __str__(self):
        return f"{self.provider.user.username} provides {self.service.name}"
    