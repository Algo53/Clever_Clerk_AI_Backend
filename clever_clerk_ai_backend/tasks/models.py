from django.db import models
from api.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo","To Do"),("in-progress","In Progress"),("done","Done")
    ]
    PRIORITY_CHOICES = [
        ("low","Low"),("medium","Medium"),("high","High"),("urgent","Urgent")
    ]
    CATEGORY_CHOICES = [
        ("Work", "Work"),
        ("Personal", "Personal"),
        ("Health", "Health"),
        ("Shopping", "Shopping"),
    ]
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title     = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority  = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="low")
    category  = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Work")
    deadline  = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class Milestone(models.Model):
    task        = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="milestones")
    title       = models.CharField(max_length=200)
    completed   = models.BooleanField(default=False)
    completedAt = models.DateTimeField(null=True, blank=True)

class ContextEntry(models.Model):
    SOURCES = [("whatsapp","WhatsApp"),("email","Email"),("notes","Notes"),("other","Other")]
    task      = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="context")
    content   = models.TextField()
    source    = models.CharField(max_length=20, choices=SOURCES)
    timestamp = models.DateTimeField(auto_now_add=True)