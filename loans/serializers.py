from rest_framework import serializers
import loans.models as models


class RequestHeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RequestHeader
        fields = ('CFRequestId', 'RequestDate', 'CFApiUserId',
                  'CFApiPassword', 'IsTestLead')


class SelfReportedCashFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SelfReportedCashFlow
        fields = ('AnnualRevenue', 'MonthlyAverageBankBalance',
                  'MonthlyAverageCreditCardVolume')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        fields = ('Address1', 'Address2', 'City', 'State', 'Zip')


class BusinessSerializer(serializers.ModelSerializer):

    SelfReportedCashFlow = SelfReportedCashFlowSerializer(
        many=False)
    Address = AddressSerializer(many=False)

    class Meta:
        model = models.Business
        fields = ('Name', 'SelfReportedCashFlow', 'Address', 'TaxID', 'Phone',
                  'NAICS', 'HasBeenProfitable', 'HasBankruptedInLast7Years', 'InceptionDate')


class OwnerSerializer(serializers.ModelSerializer):

    HomeAddress = AddressSerializer(many=False)

    class Meta:
        model = models.Owner
        fields = ('Name', 'FirstName', 'LastName', 'Email', 'HomeAddress',
                  'DateOfBirth', 'HomePhone', 'SSN', 'PercentageOfOwnership')


class CFApplicationDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CFApplicationData
        fields = ('RequestedLoanAmount', 'StatedCreditHistory',
                  'LegalEntityType', 'FilterID')


class LoanApplicationSerializer(serializers.ModelSerializer):

    RequestHeader = RequestHeaderSerializer(many=False)
    Business = BusinessSerializer(many=False)
    Owners = OwnerSerializer(many=True)
    CFApplicationData = CFApplicationDataSerializer(many=False)

    class Meta:
        model = models.LoanApplication
        fields = ('RequestHeader', 'Business',
                  'Owners', 'CFApplicationData')


# ------------------------------------- #


class StatusSerializer(serializers.Serializer):
    loanapp_id = serializers.IntegerField()
