from django.db import models


class RequestHeader(models.Model):

    CFRequestId = models.CharField(max_length=32)
    RequestDate = models.DateTimeField()

    CFApiUserId = models.CharField(max_length=32, null=True)
    CFApiPassword = models.CharField(max_length=128, null=True)

    IsTestLead = models.BooleanField(default=False)


class SelfReportedCashFlow(models.Model):
    AnnualRevenue = models.DecimalField(decimal_places=2, max_digits=16)
    MonthlyAverageBankBalance = models.DecimalField(
        decimal_places=2, max_digits=16)
    MonthlyAverageCreditCardVolume = models.DecimalField(
        decimal_places=2, max_digits=16)


class Address(models.Model):
    Address1 = models.CharField(max_length=512)
    Address2 = models.CharField(max_length=512, null=True)
    City = models.CharField(max_length=256)
    State = models.CharField(max_length=32)
    Zip = models.CharField(max_length=16)


class Business(models.Model):
    Name = models.CharField(max_length=256)
    SelfReportedCashFlow = models.ForeignKey(
        SelfReportedCashFlow, on_delete=models.CASCADE, null=True)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    TaxID = models.CharField(max_length=16)
    Phone = models.CharField(max_length=16)
    NAICS = models.CharField(max_length=8)
    HasBeenProfitable = models.BooleanField(default=False)
    HasBankruptedInLast7Years = models.BooleanField(default=True)
    InceptionDate = models.DateTimeField()


class Owner(models.Model):
    Name = models.CharField(max_length=32)
    FirstName = models.CharField(max_length=32)
    LastName = models.CharField(max_length=32)
    Email = models.EmailField()
    HomeAddress = models.ForeignKey(Address, on_delete=models.CASCADE)
    DateOfBirth = models.DateTimeField()
    HomePhone = models.CharField(max_length=16)
    SSN = models.CharField(max_length=9)
    PercentageOfOwnership = models.DecimalField(
        decimal_places=2, max_digits=5, null=True)


class CFApplicationData(models.Model):
    RequestedLoanAmount = models.DecimalField(decimal_places=2, max_digits=16)
    StatedCreditHistory = models.IntegerField()
    LegalEntityType = models.CharField(max_length=16)
    FilterID = models.CharField(max_length=8)


class LoanApplication(models.Model):
    RequestHeader = models.ForeignKey(
        RequestHeader, on_delete=models.CASCADE, null=True)
    Business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    Owners = models.ManyToManyField(Owner)
    CFApplicationData = models.ForeignKey(
        CFApplicationData, on_delete=models.CASCADE, null=True)
