from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Division(models.Model):
    CATEGORY = (
        ('district', 'District'),
        ('possession', 'Possession'),
        ('state', 'State'),
        ('territory', 'Territory'),
    )
    category = models.CharField(max_length=25, null=False, blank=False,
                                choices=CATEGORY, default='state')
    name = models.CharField(max_length=100, null=False, blank=False,
                            unique=True)
    abbreviation = models.CharField(max_length=2, null=False, blank=False,
                                    unique=True)
    capital_city = models.CharField(max_length=100, null=False, blank=False)
    data_available = models.BooleanField(default=False)
    DATA_RESTRICTIONS = (
        ('no', 'No'),
        ('yes', 'Yes'),
        ('unknown', 'Unknown'),
    )
    data_restrictions = models.CharField(max_length=10, default='unknown',
                                         null=False, blank=False,
                                         choices=DATA_RESTRICTIONS)
    DATA_REFRESH = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('semi-annually', 'Semi-Annually'),
        ('annually', 'Annually'),
        ('unknown', 'Unknown'),
    )
    data_refresh = models.CharField(max_length=15, default='Unknown',
                                    null=False, blank=False,
                                    choices=DATA_REFRESH)
    data_cost = models.IntegerField(default=0, null=False, blank=False)
    data_source = models.CharField(max_length=100, null=False, blank=False,
                                   default="Department of State")
    data_url = models.URLField(null=True, blank=True)
    data_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    slug = models.SlugField(max_length=105, null=False, blank=False,
                            unique=True)
    is_published = models.BooleanField(default=False)
    last_updated = models.DateTimeField(default=datetime.now(), null=False,
                                        blank=False)

    def __str__(self):
        return self.name
