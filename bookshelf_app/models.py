from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(
        max_length = 64, 
        null = False, 
        default = "Tidak Berjudul")
    description = models.CharField(
        max_length = 128, 
        null = False, 
        default = "Tidak Berjudul")

    def as_dict(self):
        ''' return data with dictionary format (serialize each object returned not all of the objects returned) '''

        return dict(
            id = self.id,
            title = self.title,
            description = self.description
        )