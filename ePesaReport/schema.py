import graphene
from pesaManagement.models import PesaManagement
from .epesaReport_dto import  EpesaReportResponseObject, EpesaReportFilteringInputObject, EpesaReportResponseObjectType, TopThreeAmountMonthInputObject, TopThreeAmountMonthResponseObject, TopThreeAmountPerDayInputObject, TopThreeAmountPerDayObjectType, TopThreeAmountPerDayResponseObject, TopThreeAmountYearInputObject, TopThreeAmountYearResponseObject
from uaa.models import UsersProfiles
from response.Response import ResponseObject
from datetime import datetime
class Query(graphene.ObjectType):
    date_now = datetime.now()
    get_all_dashboard_report = graphene.Field(EpesaReportResponseObjectType, filtering =EpesaReportFilteringInputObject(required=True) )
    get_all_three_maximum_amount_in_day = graphene.Field(TopThreeAmountPerDayResponseObject, filtering = TopThreeAmountPerDayInputObject())
    get_all_three_maximum_amount_in_month = graphene.Field(TopThreeAmountMonthResponseObject,filtering=TopThreeAmountMonthInputObject())
    get_all_three_maximum_amount_in_year = graphene.Field(TopThreeAmountYearResponseObject, filtering = TopThreeAmountYearInputObject())

    def resolve_get_all_dashboard_report(self,info, filtering=None):
        total_amount_today=0
        total_amount_this_week=0
        total_amount_this_month =0
        total_amount_this_year =0
        date_now = datetime.now()
        day= date_now.strftime('%d')
        month = date_now.strftime('%m')
        year = date_now.strftime('%Y')
        week = date_now.isocalendar()[1]
        user = UsersProfiles.objects.filter(user_unique_id=filtering.user_unique_id).first()
        all_user_data =PesaManagement.objects.filter(user=user).all()
        for data in all_user_data:
            if day == data.spend_date.strftime('%d'):
                total_amount_today +=data.amount_spend
                print("{:0,.2f}".format((total_amount_today)))
            if month == data.spend_date.strftime('%m'):
                total_amount_this_month +=data.amount_spend
            if week == data.spend_date.isocalendar()[1]:
                total_amount_this_week +=data.amount_spend
            if year == data.spend_date.strftime('%Y'):
                total_amount_this_year += data.amount_spend
        data=EpesaReportResponseObject(
            total_amount_today ="{:0,.2f}".format(float(total_amount_today)),
            total_amount_this_week = "{:0,.2f}".format(float(total_amount_this_week)),
            total_amount_this_month= "{:0,.2f}".format(float(total_amount_this_month)),
            total_amount_this_year= "{:0,.2f}".format(float(total_amount_this_year))
        )
        l = [1000, 298, 3579, 100, 200, -45, 900]
        n = 4
        
        l.sort()
        print(l[-n:])
        return EpesaReportResponseObjectType(response = ResponseObject.get_response(id='2'), data = data)
    
    def resolve_get_all_three_maximum_amount_in_day(self, info , filtering=None, **kwargs):
        user = UsersProfiles.objects.filter(user_unique_id=filtering.user_unique_id).first()
        user_data = PesaManagement.objects.filter(user = user).all()
        print(user_data)
        # user_data.get()
        last_three_days = []
        larget_amont =[]
        reason = []
        for data in user_data:
            data_new = data.spend_date
        for i in range(0, 3):
            max1 = 0
            days =0
            month =0
            year = 0
            for data in user_data:
                if data.amount_spend>max1:
                    max1 = data.amount_spend
                    days = data.spend_date.strftime('%d')
                # data.delete(max1)
                last_three_days.append(days)
                larget_amont.append(max1)
                print(larget_amont)
                i+=1
        # for j in range(len(list1)):
        #     if list1[j] > max1:
        #         max1 = list1[j]
 
        # list1.remove(max1)
        # final_list.append(max1)


schema = graphene.Schema(query=Query)