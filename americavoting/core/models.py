from datetime import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now


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
    data_refresh = models.CharField(max_length=15, default='unknown',
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
    DATA_STATUS = (
        ('in progress', 'In Progress'),
        ('published', 'Published'),
        ('unavailable', 'Unavailable'),
        ('under review', 'Under Review'),
    )
    data_status = models.CharField(max_length=25, null=False, blank=False,
                                   default='unavailable', choices=DATA_STATUS)
    is_published = models.BooleanField(default=False)
    # TODO: Should this be last edited, as it's only the model, not the data?
    last_updated = models.DateTimeField(default=now, null=False,
                                        blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.last_updated = datetime.now()  # Is the above redundant?
        super(Division, self).save(*args, **kwargs)


class PoliticalParty(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'political parties'


def data_set_location(instance, filename):
    # file will be uploaded to MEDIA_ROOT/data/<division>/<filename>
    return 'data/{0}/{1}-{2}'.format(instance.division.name.lower(),
                                 instance.upload_date, filename)


class DataSet(models.Model):

    # TODO: Delete file when deleting DataSet instance

    name = models.CharField(max_length=50)
    data_file = models.FileField(upload_to=data_set_location)
    division = models.ForeignKey(Division)
    upload_date = models.DateField(default=now, null=False, blank=False)

    def __str__(self):
        return self.name
