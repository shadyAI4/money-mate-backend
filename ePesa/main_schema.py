import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from graphene_federation import build_schema

# BELOW ARE THE MUTATIONS AND QUERIES
from pesaManagement.schema import Query as pesa_query
from pesaManagement.views import Mutation as pesa_mutation

from ePesaReport.schema import Query as report_query

from uaa.schema import Query as uaa_query
from uaa.views import Mutation as uaa_mutation

class Query(pesa_query,uaa_query,report_query, ObjectType):
    pass

class Mutation(pesa_mutation,uaa_mutation, ObjectType):
    pass

schema = build_schema(query=Query, mutation=Mutation)