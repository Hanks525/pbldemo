from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('academic', '学术活动'),
        ('cultural', '文化活动'),
        ('sports', '体育活动'),
        ('social', '社交活动'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    time = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publisher = models.CharField(max_length=100)
    image = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.author}: {self.content[:20]}'

class Favorite(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='favorites')
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['activity', 'user_id']
    
    def __str__(self):
        return f'User {self.user_id} favorited {self.activity.title}'

class Registration(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='registrations')
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['activity', 'user_id']
    
    def __str__(self):
        return f'User {self.user_id} registered for {self.activity.title}'
