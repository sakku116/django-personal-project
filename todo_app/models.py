from django.db import models

# Create your models here.
class Todo(models.Model):
    name = models.CharField(max_length=128, null=False, default='tidak diketahui')
    created_at = models.DateTimeField(auto_now_add=True) # automatic but not autoupdate
    updated_at = models.DateTimeField(auto_now=True) # automatic and autoupdate

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }