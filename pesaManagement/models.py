import uuid
from django.db import models

from uaa.models import UsersProfiles


# Create your models here.

class PesaManagement(models.Model):
    user = models.ForeignKey(UsersProfiles, on_delete = models.PROTECT)
    spends_uniqueId = models.UUIDField(editable = False, unique = True, default = uuid.uuid4, primary_key=True)
    amount_spend = models.DecimalField(max_digits = 10000, decimal_places=2)
    service_or_staff_spend = models.CharField(max_length = 255, null=False, blank = False)
    reason_of_spend = models.TextField()
    spend_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.service_or_staff_spend
    
    class Meta:
        db_table ="pesa_management"
        ordering =['-spend_date']
        