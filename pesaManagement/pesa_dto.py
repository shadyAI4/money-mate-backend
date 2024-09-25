import graphene
from response import Response

class PesaInputObject(graphene.InputObjectType):
    user_unique_id = graphene.String()
    amount_spend = graphene.Decimal()
    service_or_staff_spend = graphene.String()
    reason_of_spend = graphene.String()


class PesaObjectType(graphene.ObjectType):
    spends_uniqueId = graphene.String()
    amount_spend = graphene.Decimal()
    service_or_staff_spend = graphene.String()
    reason_of_spend = graphene.String()
    spend_date = graphene.String()

class PesaResponseObject(graphene.ObjectType):
    response = graphene.Field(Response.ResponseObject)
    data = graphene.List(PesaObjectType)


class PesaFilteringInput(graphene.InputObjectType):
    spends_uniqueId = graphene.String()


class PesaUpdateInputObject(graphene.InputObjectType):
    spends_uniqueId = graphene.String()
    amount_spend = graphene.Decimal()
    service_or_staff_spend = graphene.String()
    reason_of_spend = graphene.String()