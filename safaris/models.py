from django.db import models

# Create your models here.
class Payment(models.Model):
    # user = models.ForeignKey( Profile, blank=True , null=True, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=100)
    phone_number =models.PositiveIntegerField(default=254799735661)

    def __str__(self):
        return f'{self.name} payment'

    def save_payment(self):
        self.save()