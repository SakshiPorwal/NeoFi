from django.db import models
from django.contrib.auth.models import User
from noteapp.models import CustomUser, Note
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class NoteChange(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField()
    changed_at = models.DateTimeField(auto_now_add=True)


#Data Model
    
class CustomUser(AbstractUser):
    pass


class Share(models.Model):
    shared_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shared_by')
    shared_with = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shared_with')
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.shared_by} shared note "{self.note}" with {self.shared_with}'
