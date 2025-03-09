from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)  # Post title
    content = models.TextField()  # Post content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the post is created
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who created the post
    
    def __str__(self):
        return self.title  # Display the title when the object is called in admin or other views

