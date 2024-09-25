import graphene
from graphene import ObjectType
from response.Response import ResponseObject

class EpesaReportFilteringInputObject(graphene.InputObjectType):
    user_unique_id = graphene.String()

class EpesaReportResponseObject(graphene.ObjectType):
    total_amount_today=graphene.String()
    total_amount_this_week = graphene.String()
    total_amount_this_month = graphene.String()
    total_amount_this_year = graphene.String()

class EpesaReportResponseObjectType(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.Field(EpesaReportResponseObject)


class TopThreeAmountPerDayInputObject(graphene.InputObjectType):
    user_unique_id = graphene.String()

class TopThreeAmountPerDayObjectType(graphene.ObjectType):
    day = graphene.String()
    amount = graphene.String()
    reason = graphene.String()

class TopThreeAmountPerDayResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(TopThreeAmountPerDayObjectType)


class TopThreeAmountMonthInputObject(graphene.InputObjectType):
    user_unique_id = graphene.String()

class TopThreeAmountMonthObjectType(graphene.ObjectType):
    month = graphene.String()
    amount = graphene.String()
    reason = graphene.String()

class TopThreeAmountMonthResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(TopThreeAmountMonthObjectType)


class TopThreeAmountYearInputObject(graphene.InputObjectType):
    user_unique_id = graphene.String()

class TopThreeAmountYearObjectType(graphene.ObjectType):
    year = graphene.String()
    amount = graphene.String()
    reason = graphene.String()

class TopThreeAmountYearResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(TopThreeAmountYearObjectType)