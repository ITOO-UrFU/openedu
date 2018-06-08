from django.contrib import admin

from .models import Minor, Bid, Author, OOPBid, QuoteBid


@admin.register(Minor)
class MinorAdmin(admin.ModelAdmin):
    list_display = ('published', 'name', 'author', 'startdate', 'enddate', 'active')
    list_filter = ('published',)
    filter_horizontal = ("authors",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('minor', 'name', 'email', 'phone', 'created_at', 'done')
    readonly_fields = ('minor', 'name', 'email', 'phone', 'created_at')


@admin.register(OOPBid)
class OOPBidAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'program', 'message', 'created_at', 'updated_at', 'done')
    readonly_fields = ('name', 'email', 'phone', 'program', 'message', 'created_at', 'updated_at')


@admin.register(QuoteBid)
class QuoteBidAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'course', 'agreement', 'created_at', 'updated_at', 'quoted', 'done')
    readonly_fields = ('name', 'email', 'phone', 'agreement', 'created_at', 'updated_at')
    search_fields = ('name', "email", 'phone')
