from django.contrib import admin

from .models import Division


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    search_fields = ["name", "abbreviation"]
    list_display = ["name", "capital_city"]
    pass
