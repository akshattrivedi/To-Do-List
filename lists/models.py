from django.contrib.auth.models import User
from django.db import models

class Todo(models.Model):
    description = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, null=True, related_name="todos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.description

    def close(self):
        self.is_finished = True
        self.save()

    def reopen(self):
        self.is_finished = False
        self.save()

