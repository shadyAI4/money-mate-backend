from .pesa_dto import PesaInputObject, PesaObjectType , PesaResponseObject
from .models import PesaManagement

class PesaBuilder:

    @staticmethod
    def resolve_get_pesa_management_data(id):
        pesa_data = PesaManagement.objects.filter(spends_uniqueId = id).first()

        if id is not None:
            if pesa_data:
                return PesaObjectType(
                    spends_uniqueId = pesa_data.spends_uniqueId,
                    amount_spend = pesa_data.amount_spend,
                    service_or_staff_spend = pesa_data.service_or_staff_spend,
                    reason_of_spend = pesa_data.reason_of_spend,
                    spend_date = pesa_data.spend_date
                )
            else:
                return PesaObjectType()
        else:
            return PesaObjectType()

     
    