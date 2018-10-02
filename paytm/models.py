from django.db import models

# Create your models here.

class PaytmDataBase(models.Model):

    order_id = models.CharField(max_length=150, unique=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    checksumhash = models.CharField(max_length=255)
    txn_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.order_id)

# class PaytmRefundDataBase(models.Model):
#     order_id = models.PositiveIntegerField()
#     checksumhash = models.CharField(max_length=255)

#     def __str__(self):
#         return str(self.order_id)