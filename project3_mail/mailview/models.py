from typing import Any
from django.db import models
from user.models import User
# Create your models here.
class Email(models.Model):
    user= models.ForeignKey(User, on_delete=models.PROTECT, related_name='owner', null= True)
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_mail', null= True)
    recipients= models.ManyToManyField(User, related_name='receive_mail', blank=True)
    subject= models.CharField(max_length=128)
    body= models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True)
    read= models.BooleanField(default= False)
    archived= models.BooleanField(default= False)

    def __str__(self):
        return f"Mail of {self.user}"
    
    def serialize(self):
        recipients= self.recipients.all()
        emails= []
        for recipient in recipients:
            emails.append(recipient.email)
        return {
            'id': self.pk,
            'user': self.user.email,
            'sender': self.sender.email,
            'recipients': emails,
            'subject': self.subject,
            'body': self.body,
            'timestamp': self.timestamp.strftime("%B %d %Y, %H:%M %p"),
            'read': self.read,
            'archived': self.archived
        }
    






