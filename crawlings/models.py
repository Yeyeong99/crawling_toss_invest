from django.db import models

# Create your models here.
class Comment(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.CharField(max_length=200)
    comment = models.TextField()
    saved_at = models.DateTimeField(auto_now_add=True)

class CommentAnalysis(models.Model):
    company_name = models.CharField(max_length=100)
    analysis_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)