from django.contrib import admin
from .models import LoanApplication, RequestHeader, Business, Owner, CFApplicationData, SelfReportedCashFlow, Address


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(RequestHeader)
class RequestHeader(admin.ModelAdmin):
    pass


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(CFApplicationData)
class CFApplicationData(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(SelfReportedCashFlow)
class SelfReportedCashFlowAdmin(admin.ModelAdmin):
    pass
