import random
import graphene
from pesaManagement.models import PesaManagement
from .epesaReport_dto import  EpesaReportResponseObject, EpesaReportFilteringInputObject, EpesaReportResponseObjectType, TopThreeAmountMonthInputObject, TopThreeAmountMonthResponseObject, TopThreeAmountPerDayInputObject, TopThreeAmountPerDayObjectType, TopThreeAmountPerDayResponseObject, TopThreeAmountYearInputObject, TopThreeAmountYearResponseObject
from uaa.models import UsersProfiles
from response.Response import ResponseObject
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate,  TruncMonth, TruncYear
from django.db.models import Sum
from django.utils import timezone

class Query(graphene.ObjectType):
    date_now = datetime.now()
    get_all_dashboard_report = graphene.Field(EpesaReportResponseObjectType, filtering =EpesaReportFilteringInputObject(required=True) )
    get_all_three_maximum_amount_in_day = graphene.Field(TopThreeAmountPerDayResponseObject, filtering = TopThreeAmountPerDayInputObject())
    get_all_three_maximum_amount_in_month = graphene.Field(TopThreeAmountMonthResponseObject,filtering=TopThreeAmountMonthInputObject())
    get_all_three_maximum_amount_in_year = graphene.Field(TopThreeAmountYearResponseObject, filtering = TopThreeAmountYearInputObject())

    def resolve_get_all_dashboard_report(self,info, filtering=None):
        print("this is the month",datetime.now().strftime('%m'))
        jan =0 ;feb =0 ;mar =0 ;apli=0 ;may=0 ;june=0 ;july=0 ;agust=0 ;sep=0; oct =0; nov=0; dec=0
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
        for data in all_user_data:
            print("spend data", data.spend_date)
            if '01' == data.spend_date.strftime('%m'):
                jan+=data.amount_spend
            if '02' == data.spend_date.strftime('%m'):
                feb+=data.amount_spend
            if '03' == data.spend_date.strftime('%m'):
                mar+=data.amount_spend
            if '04' == data.spend_date.strftime('%m'):
                apli+=data.amount_spend
            if '05' == data.spend_date.strftime('%m'):
                may+=data.amount_spend
            if '06' == data.spend_date.strftime('%m'):
                june+=data.amount_spend
            if '07' == data.spend_date.strftime('%m'):
                july+=data.amount_spend
            if '08' == data.spend_date.strftime('%m'):
                agust+=data.amount_spend
            if '09' == data.spend_date.strftime('%m'):
                print("teeee")
                sep+=data.amount_spend
            if '10' == data.spend_date.strftime('%m'):
                oct+=data.amount_spend
            if '11' == data.spend_date.strftime('%m'):
                nov+=data.amount_spend
            if '12' == data.spend_date.strftime('%m'):
                dec+=data.amount_spend

        spenPerDay = (PesaManagement.objects
                .annotate(date=TruncDate('spend_date')).values('date')
                .annotate(total_spend=Sum('amount_spend')).order_by('date')
                )
        # Convert the result to a dictionary for easier lookup
        spend_per_day = {entry['date']: entry['total_spend'] for entry in spenPerDay}

        # Find the first and last days in the data
        if spenPerDay.exists():
            first_day = spenPerDay.first()['date']
            last_day = spenPerDay.last()['date']
        else:
            # If no data is found, use the current date as both first and last day
            first_day = last_day = datetime.today().date()

        # Generate all days between the first and last day
        current_day = first_day
        all_days = []
        while current_day <= last_day:
            all_days.append(current_day)
            current_day += timedelta(days=1)  # Move to the next day

        # Fill missing days with 0 spend
        response_data = []
        for day in all_days:
            response_data.append({
                'day': day,
                'amount': spend_per_day.get(day, random.randint(1000,100000))  # Return 0 if the day is missing
            })
        today = timezone.now()

    # Get max spends for the last 5 days
        max_days_spending = (
            PesaManagement.objects
            .filter(spend_date__gte=today - timedelta(days=5))
            .annotate(date=TruncDate('spend_date'))
            .values('date')
            .annotate(total_spend=Sum('amount_spend'))
            .order_by('-total_spend')[:5]
        )

        # Get max spends for the last 5 months
        max_months_spending = (
            PesaManagement.objects
            .filter(spend_date__gte=today - timedelta(days=30 * 5))  # Approximation for 5 months
            .annotate(month=TruncMonth('spend_date'))
            .values('month')
            .annotate(total_spend=Sum('amount_spend'))
            .order_by('-total_spend')[:5]
        )

        # Get max spends for the last 3 years
        max_years_spending = (
            PesaManagement.objects
            .filter(spend_date__gte=today - timedelta(days=365 * 3))  # 3 years
            .annotate(year=TruncYear('spend_date'))
            .values('year')
            .annotate(total_spend=Sum('amount_spend'))
            .order_by('-total_spend')[:3]
        )
        data=EpesaReportResponseObject(
            total_amount_today ="{:0,.2f}".format(float(total_amount_today)),
            total_amount_this_week = "{:0,.2f}".format(float(total_amount_this_week)),
            total_amount_this_month= "{:0,.2f}".format(float(total_amount_this_month)),
            total_amount_this_year= "{:0,.2f}".format(float(total_amount_this_year)),
            spends_per_month = [
                {
                    'amount':jan,
                    'month' :'Janury'
                },
                {
                    'amount':feb,
                    'month' :'February'
                },
                {
                    'amount':mar,
                    'month' :'March'
                },
                {
                    'amount':apli,
                    'month' :'April'
                },
                {
                    'amount':may,
                    'month' :'May'
                },
                {
                    'amount':june,
                    'month' :'June'
                },
                {
                    'amount':july,
                    'month' :'July'
                },
                {
                    'amount':agust,
                    'month' :'August'
                },
                {
                    'amount':sep,
                    'month' :'Septermber'
                },
                {
                    'amount':oct,
                    'month' :'October'
                },
                {
                    'amount':nov,
                    'month' :'November'
                },
                {
                    'amount':dec,

                    'month' :'December'
                }
            ],
            spends_per_day=response_data,
            max_day_spends= max_days_spending,
            max_month_spends=max_months_spending,
            max_year_spends= max_years_spending
    
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


schema = graphene.Schema(query=Query)