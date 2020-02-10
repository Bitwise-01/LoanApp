from django.test import TestCase
import loans.models as models
from decimal import Decimal
from datetime import datetime, timezone


class RequestHeaderTestCase(TestCase):

    pk = None

    def setUp(self):
        self.pk = models.RequestHeader.objects.create(
            CFRequestId='500653901',
            RequestDate='2019-06-26T23:05:41.2898238Z',
            CFApiUserId='Test',
            CFApiPassword='Test',
            IsTestLead=True
        ).id

    def test_RequestHeader_fields_set(self):
        request_header = models.RequestHeader.objects.get(id=self.pk)

        self.assertEqual(request_header.CFRequestId, '500653901')
        self.assertEqual(str(request_header.RequestDate),
                         '2019-06-26 23:05:41.289823+00:00')

        self.assertEqual(request_header.CFApiUserId, 'Test')
        self.assertEqual(request_header.CFApiPassword, 'Test')
        self.assertEqual(request_header.IsTestLead, True)


class SelfReportedCashFlow(TestCase):

    pk = None

    def setUp(self):
        self.pk = models.SelfReportedCashFlow.objects.create(
            AnnualRevenue=3.14,
            MonthlyAverageBankBalance=2.72,
            MonthlyAverageCreditCardVolume=1.62
        ).id

    def test_SelfReportedCashFlow_fields_set(self):
        self_reported_cash_flow = models.SelfReportedCashFlow.objects.get(
            id=self.pk)

        self.assertEqual(self_reported_cash_flow.AnnualRevenue,
                         Decimal(str(3.14)))

        self.assertEqual(
            self_reported_cash_flow.MonthlyAverageBankBalance, Decimal(str(2.72)))

        self.assertEqual(self_reported_cash_flow.MonthlyAverageCreditCardVolume,
                         Decimal(str(1.62)))


class AddressTestCase(TestCase):
    pk = None

    def setUp(self):
        self.pk = models.Address.objects.create(
            Address1='123 Main St',
            Address2='456 Main St',
            City='Los Angeles',
            State='CA',
            Zip='90042'
        ).id

    def test_Address_fields_set(self):
        address = models.Address.objects.get(id=self.pk)

        self.assertEqual(address.Address1, '123 Main St')

        self.assertEqual(address.Address2, '456 Main St')

        self.assertEqual(address.City, 'Los Angeles')

        self.assertEqual(address.State, 'CA')

        self.assertEqual(address.Zip, '90042')


class BusinessTestCase(TestCase):
    pk = None

    def setUp(self):
        self_reported_cash_flow = models.SelfReportedCashFlow.objects.create(
            AnnualRevenue=3.14,
            MonthlyAverageBankBalance=2.72,
            MonthlyAverageCreditCardVolume=1.62
        )

        address = models.Address.objects.create(
            Address1='123 Main St',
            Address2='456 Main St',
            City='Los Angeles',
            State='CA',
            Zip='90042'
        )

        self.pk = models.Business.objects.create(
            Name='Microsoft',
            SelfReportedCashFlow=self_reported_cash_flow,
            Address=address,
            TaxID='31415',
            Phone='555-555-5555',
            NAICS='79232',
            HasBeenProfitable=True,
            HasBankruptedInLast7Years=False,
            InceptionDate='2008-06-28T23:04:03.5507585+00:00'
        ).id

    def test_Business_fields_set(self):
        business = models.Business.objects.get(id=self.pk)

        self.assertEqual(business.Name, 'Microsoft')

        self.assertEqual(business.TaxID, '31415')

        self.assertEqual(business.HasBeenProfitable, True)

        self.assertEqual(business.HasBankruptedInLast7Years, False)

        date = datetime(2008, 6, 28, 23, 4, 3, 550758, tzinfo=timezone.utc)
        self.assertEqual(business.InceptionDate, date)


class OwnerTestCase(TestCase):

    pk = None

    def setUp(self):
        home_address = models.Address.objects.create(
            Address1='123 Main St',
            Address2='456 Main St',
            City='Los Angeles',
            State='CA',
            Zip='90042'
        )

        self.pk = models.Owner.objects.create(
            Name='Nikki Lee',
            FirstName='Nikki',
            LastName='Lee',
            Email='Nikkilee@gmail.com',
            HomeAddress=home_address,
            DateOfBirth='1992-08-11T08:27:46.5507585+00:00',
            HomePhone='555-555-5555',
            SSN='142-68-8321',
            PercentageOfOwnership=80.20
        ).id

    def test_Ower_fields_set(self):
        owner = models.Owner.objects.get(id=self.pk)

        self.assertEqual(owner.Name, 'Nikki Lee')
        self.assertEqual(owner.FirstName, 'Nikki')
        self.assertEqual(owner.LastName, 'Lee')

        self.assertEqual(owner.Email, 'Nikkilee@gmail.com')

        date = datetime(1992, 8, 11, 8, 27, 46, 550758, tzinfo=timezone.utc)
        self.assertEqual(owner.DateOfBirth, date)

        self.assertEqual(owner.HomePhone, '555-555-5555')
        self.assertEqual(owner.SSN, '142-68-8321')

        self.assertEqual(owner.PercentageOfOwnership, Decimal(str(80.20)))


class CFApplicationDataTestCase(TestCase):

    pk = None

    def setUp(self):
        self.pk = models.CFApplicationData.objects.create(
            RequestedLoanAmount=1248.00,
            StatedCreditHistory=1,
            LegalEntityType='LLC',
            FilterID='897079'
        ).id

    def test_CFApplicationData_fields_set(self):
        '''Make sure every field is set.
        '''

        cf_application_data = models.CFApplicationData.objects.get(id=self.pk)

        self.assertEqual(
            cf_application_data.RequestedLoanAmount,
            Decimal(str(1248.00))
        )

        self.assertEqual(
            cf_application_data.StatedCreditHistory,
            1
        )

        self.assertEqual(
            cf_application_data.LegalEntityType,
            'LLC'
        )

        self.assertEqual(
            cf_application_data.FilterID,
            '897079'
        )
