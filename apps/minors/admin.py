from django.contrib import admin

from .models import Minor, Bid, Author, OOPBid


@admin.register(Minor)
class MinorAdmin(admin.ModelAdmin):
    list_display = ('published', 'name', 'author', 'startdate', 'enddate')
    list_filter = ('published', )
    filter_horizontal = ("authors", )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('minor', 'name', 'email', 'phone', 'created_at', 'done')
    readonly_fields = ('minor', 'name', 'email', 'phone', 'created_at')


@admin.register(OOPBid)
class OOPBidAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'program', 'message', 'done')
    readonly_fields = ('name', 'email', 'phone', 'program', 'message')
