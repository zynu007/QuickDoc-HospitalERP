from django.db import models
from django.conf import settings
from django.utils.text import Truncator

class Category(models.TextChoices):
    MENTAL_HEALTH = 'mental_health', 'Mental Health'
    HEART_DISEASE = 'heart_disease', 'Heart Disease'
    DIABETES = 'diabetes', 'Diabetes'
    CANCER = 'cancer', 'Cancer'

class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )
    summary = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def truncated_summary(self):
        words = self.summary.split()
        if len(words) > 15:
            return ' '.join(words[:15]) + '...'
        return self.summary
    
    class Meta:
        ordering = ['-created_at']