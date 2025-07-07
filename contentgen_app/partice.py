from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField  # If using Postgres

User = get_user_model()

class GeneratedContent(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_contents')
    prompt = models.TextField()
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    tokens_used = models.IntegerField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    metadata = models.JSONField(blank=True, null=True)  # for API params, etc
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prompt[:50]}... ({self.status})"
