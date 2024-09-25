from .models import PesaManagement
from .pesa_dto import PesaResponseObject, PesaFilteringInput, PesaObjectType
from .pesa_builder import PesaBuilder
from graphene_django import DjangoObjectType
import graphene
from  graphene import ObjectType
from response.Response import ResponseObject

class Query(ObjectType):

    get_all_pesa_data = graphene.Field(PesaResponseObject, filtering = PesaFilteringInput())
    get_pesa_data = graphene.Field(PesaObjectType, filtering = PesaFilteringInput())

    def resolve_get_all_pesa_data(self, info, filtering=None, **kwargs):
        if filtering.spends_uniqueId is None:
            return PesaResponseObject(response = ResponseObject.get_response(id='13'), data = None)
        else :
            pesa_data = PesaManagement.objects.all().values("spends_uniqueId")
            pesa_data_builded = PesaBuilder.resolve_get_pesa_management_data(pesa_data.spends_uniqueId)

            return PesaResponseObject(response = ResponseObject.get_response(id='2'), data = pesa_data_builded)
    
    def resolve_get_pesa_data(self, info, filtering =None, **kwargs):
        if filtering.spends_uniqueId is None:
            return self(response = ResponseObject.get_response(id='13'), data = None)
        else:
            pesa_data = PesaManagement.objects.filter(filtering.spends_uniqueId).first()
            return self(response = ResponseObject.get_response(id='2'), data=pesa_data)
    

schema = graphene.Schema(query=Query)
