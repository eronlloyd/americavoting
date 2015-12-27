from django.contrib import admin

from .models import DataSet, Division, PoliticalParty


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ['name', 'division', 'data_file']


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'abbreviation']
    list_display = ['name', 'category', 'abbreviation', 'data_status',
                    'data_date', 'last_updated']
    list_filter = ['category', 'data_status']
    actions = ['make_published', 'make_unavailable']

    def make_published(self, request, query_set):
        rows_updated = query_set.update(data_status='published')
        if rows_updated == 1:
            message_bit = "1 division was"
        else:
            message_bit = "%s divisions were" % rows_updated
        self.message_user(request, "%s successfully marked as published."
                          % message_bit)
    make_published.short_description = "Mark selected divisions as published"

    def make_unavailable(self, request, query_set):
        rows_updated = query_set.update(data_status='unavailable')
        if rows_updated == 1:
            message_bit = "1 division was"
        else:
            message_bit = "%s divisions were" % rows_updated
        self.message_user(request, "%s successfully marked as unavailable."
                          % message_bit)
    make_unavailable.short_description = "Mark selected divisions as unavailable"


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    name = "political parties"
