import loans.models as models
import loans.serializers as serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import random

from collections import OrderedDict
from typing import List, Dict


class Update:

    @staticmethod
    def business_info(current_business: models.Business, new_business: OrderedDict) -> List[str]:
        '''Returns a list of updated fields within the business model.
        '''

        updated = []

        # current
        current_business_address = current_business.Address
        current_business_self_reported_cash_flow = current_business.SelfReportedCashFlow

        # new
        new_business_address = new_business.get('Address')
        new_business_self_reported_cash_flow = new_business.get(
            'SelfReportedCashFlow'
        )

        # compare

        # self reported cash flow
        if str(current_business_self_reported_cash_flow.AnnualRevenue) != new_business_self_reported_cash_flow.get('AnnualRevenue'):
            current_business_self_reported_cash_flow.AnnualRevenue = new_business_self_reported_cash_flow.get(
                'AnnualRevenue')
            updated.append('SelfReportedCashFlow')

        if str(current_business_self_reported_cash_flow.MonthlyAverageBankBalance) != new_business_self_reported_cash_flow.get('MonthlyAverageBankBalance'):
            current_business_self_reported_cash_flow.MonthlyAverageBankBalance = new_business_self_reported_cash_flow.get(
                'MonthlyAverageBankBalance')
            updated.append('SelfReportedCashFlow')

        if str(current_business_self_reported_cash_flow.MonthlyAverageCreditCardVolume) != new_business_self_reported_cash_flow.get('MonthlyAverageCreditCardVolume'):
            current_business_self_reported_cash_flow.MonthlyAverageCreditCardVolume = new_business_self_reported_cash_flow.get(
                'MonthlyAverageCreditCardVolume')
            updated.append('SelfReportedCashFlow')

        # address
        if current_business_address.Address1 != new_business_address.get('Address1'):
            current_business_address.Address1 = new_business_address.get(
                'Address1')
            updated.append('Address')

        if current_business_address.Address2 != new_business_address.get('Address2'):
            current_business_address.Address2 = new_business_address.get(
                'Address2')
            updated.append('Address')

        if current_business_address.City != new_business_address.get('City'):
            current_business_address.City = new_business_address.get('City')
            updated.append('Address')

        if current_business_address.State != new_business_address.get('State'):
            current_business_address.State = new_business_address.get('State')
            updated.append('Address')

        if current_business_address.Zip != new_business_address.get('Zip'):
            current_business_address.Zip = new_business_address.get('Zip')
            updated.append('Address')

        # info
        if current_business.TaxID != new_business.get('TaxID'):
            current_business.TaxID = new_business.get('TaxID')
            updated.append('TaxID')

        if current_business.Phone != new_business.get('Phone'):
            current_business.Phone = new_business.get('Phone')
            updated.append('Phone')

        if current_business.NAICS != new_business.get('NAICS'):
            current_business.NAICS = new_business.get('NAICS')
            updated.append('NAICS')

        if current_business.HasBeenProfitable != new_business.get('HasBeenProfitable'):
            current_business.HasBeenProfitable = new_business.get(
                'HasBeenProfitable')
            updated.append('HasBeenProfitable')

        if current_business.HasBankruptedInLast7Years != new_business.get('HasBankruptedInLast7Years'):
            updated.append('HasBankruptedInLasy7Years')

            current_business.HasBankruptedInLast7Years = new_business.get(
                'HasBankruptedInLast7Years')

        # save changes
        current_business.save()

        return list(set(updated))


def create_loan_app(data):
    '''Create a new load application.
    '''

    # request header
    request_header = models.RequestHeader.objects.get_or_create(
        **data.get('RequestHeader')
    )

    # business
    business_data = dict(data.get('Business'))
    business_data['Name'] = business_data['Name'].title()

    business_data['Address'] = models.Address.objects.get_or_create(
        **data.get('Business').get('Address')
    )[0]

    business_data['SelfReportedCashFlow'] = models.SelfReportedCashFlow.objects.get_or_create(
        **data.get('Business').get('SelfReportedCashFlow')
    )[0]

    business = models.Business.objects.get_or_create(**business_data)

    # owners
    owners = []
    for owner in data.get('Owners'):

        owner_data = dict(owner)
        owner_data['Name'] = owner_data['Name'].title()

        owner_data['HomeAddress'] = models.Address.objects.get_or_create(
            **owner.get('HomeAddress')
        )[0]

        owners.append(
            models.Owner.objects.get_or_create(**owner_data)[0]
        )

    cf_application_data = models.CFApplicationData.objects.get_or_create(
        **data.get('CFApplicationData')
    )

    # Create loan
    loan_data = dict(data)
    loan_data.pop('Owners')

    loan_data['Business'] = business[0]
    loan_data['RequestHeader'] = request_header[0]
    loan_data['CFApplicationData'] = cf_application_data[0]

    loan_app = models.LoanApplication.objects.get_or_create(
        **loan_data)[0]

    for owner in owners:
        loan_app.Owners.add(owner)

    return {
        'Status': 'Successfully submitted loan application',
        'loanapp_id': loan_app.id
    }


def update_loan_app(data: OrderedDict, business: models.Business) -> Dict:

    loan_app = models.LoanApplication.objects.get(Business=business)

    # current app
    current_business = business

    new_business = data.get('Business')

    business_updates = Update.business_info(current_business, new_business)

    if len(business_updates):
        status = {
            'loanapp_id': loan_app.id,
            'Status': 'Successfully updated loan application',
            'Updated': business_updates,
        }
    else:
        status = {
            'loanapp_id': loan_app.id,
            'Status': 'No changes were made',
        }

    return status


class LoanAppAPI(APIView):

    serializer_class = serializers.LoanApplicationSerializer

    def post(self, request):

        serializer = serializers.LoanApplicationSerializer(data=request.data)

        if serializer.is_valid():

            data = serializer.data
            business_name = data.get('Business')['Name'].title()

            _status = {
                'Status': 'Faild to Submit loan application'
            }

            try:
                business = models.Business.objects.get(Name=business_name)
                _status = update_loan_app(data, business)
            except models.Business.DoesNotExist:
                _status = create_loan_app(data)

            return Response(_status, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def bedside_manners():
    resp = [
        'Patience is a virtue',
        'Your application is still processing',
        'Be patient',
        'Chillax, we did not forget about you',
        'We are working as quickly as possible to get your application processed',
        'Your application has not finished processing',
    ]

    return random.choice(resp)


class StatusAPI(APIView):

    serializer_class = serializers.StatusSerializer

    def get(self, request, format=None):
        return Response()

    def post(self, request):

        serializer = serializers.StatusSerializer(data=request.data)

        if serializer.is_valid():

            data = serializer.data

            try:
                loan_app = models.LoanApplication.objects.get(
                    id=data['loanapp_id'])
                _status = {
                    'Status': bedside_manners()
                }
            except:
                _status = {
                    'Status': 'Faild to locate an application by that loanapp id'
                }

            return Response(_status, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
