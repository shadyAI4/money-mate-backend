from django.shortcuts import render

import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from uaa.models import UsersProfiles


from .models import PesaManagement
from .pesa_dto import PesaFilteringInput, PesaInputObject, PesaObjectType, PesaResponseObject, PesaUpdateInputObject
from  response.Response import ResponseObject
from .pesa_builder import PesaBuilder

class AddNewConsumption(graphene.Mutation):
    class Arguments:
        input = PesaInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(PesaObjectType)

    @classmethod
    def mutate(self, root, info, input):
        if input.user_unique_id is None:
            return self(response = ResponseObject.get_response(id='9'))
        if input.amount_spend is None:
            return self(response = ResponseObject.get_response(id='10'))
        elif input.service_or_staff_spend is None:
            return self(response = ResponseObject.get_response(id='11'))
        else:
            user_data = UsersProfiles.objects.filter(user_unique_id =input.user_unique_id).first()
            pesa_create = PesaManagement.objects.create(
                user = user_data,
                amount_spend = input.amount_spend,
                service_or_staff_spend = input.service_or_staff_spend,
                reason_of_spend = input.reason_of_spend
            )
            data = PesaBuilder.resolve_get_pesa_management_data(pesa_create.spends_uniqueId)
            return self(response = ResponseObject.get_response(id='12'), data=data)

class UpdatePesaConsumption(graphene.Mutation):
    class Arguments:
        input = PesaUpdateInputObject(required = True)
    response = graphene.Field(ResponseObject)
    data = graphene.Field(PesaObjectType)

    @classmethod
    def mutate(self, root, info, input):
        if input.spends_uniqueId is None:
            return self(response = ResponseObject.get_response(id='13'))
        
        else:
            update_pesa = PesaManagement.objects.get(spends_uniqueId = input.spends_uniqueId)
            update_pesa.amount_spend = input.amount_spend
            update_pesa.service_or_staff_spend = input.service_or_staff_spend
            update_pesa.reason_of_spend = input.reason_of_spend

            update_pesa.save()
            data = PesaBuilder.resolve_get_pesa_management_data(input.spends_uniqueId)

            return self(response = ResponseObject.get_response(id='14'), data= data)
    
class Mutation(graphene.ObjectType):
    create_new_consumetion = AddNewConsumption.Field()
    update_consumption = UpdatePesaConsumption.Field()

schema = graphene.Schema(mutation=Mutation)