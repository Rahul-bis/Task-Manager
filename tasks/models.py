from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    time_req = models.CharField(null=True, max_length=20)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=[('Work', 'Work'), ('Personal', 'Personal')])

    def __str__(self):
        return self.title
