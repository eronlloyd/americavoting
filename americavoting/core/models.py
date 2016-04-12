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


class Voter(models.Model):
    # This will be the base voter class. I still need to decide how to handle
    # fields I don't want to standardize on, yet, however. TODO

    official_id = models.IntegerField()
    slug = 'voter-registration'

    districts = models.ManyToManyField(GeoDistrict, null=True, blank=True)
    identifier = models.CharField(max_length=100, blank=True)
    political_party = models.ForeignKey(PoliticalParty, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    # last_name_prefix = models.CharField(max_length=30, default="",
    # blank=True)
    last_name = models.CharField(max_length=30)
    former_name = models.CharField(max_length=30, blank=True)
    alias = models.CharField(max_length=30, blank=True)
    GENERATION_IDENTIFIER = (
        (u'Jr.', u'Jr.'),
        (u'Sr.', u'Sr.'),
        (u'I', u'I'),
        (u'II', u'II'),
        (u'III', u'III'),
    )
    generation_identifier = models.CharField(max_length=10,
                                             choices=GENERATION_IDENTIFIER,
                                             blank=True)
    # suffix = models.CharField(max_length=30, blank=True)
    # general_suffix = models.CharField(max_length=30, blank=True)
    # TODO: Now that we have the 50+ Facebook options...
    GENDER = (
        (u'Unknown', u'Unknown'),
        (u'Female', u'Female'),
        (u'Male', u'Male'),
    )
    gender = models.CharField(max_length=8, choices=GENDER,
                              default="Unknown", blank=True)
    RACE = (
        ('White', 'White'),
        ('Black', 'Black'),
        ('Latino', 'Latino'),
        ('Asian/Pacific Islander', 'Asian/Pacific Islander'),
        ('Native American', 'Native American'),
        ('Mixed/Other', 'Mixed/Other'),
    )
    race = models.CharField(max_length=30, blank=True, choices=RACE)
    # nationality = models.CharField(max_length=30, blank=True)
    # birth_place = models.CharField(max_length=30, blank=True)
    # This can be required later, depending on the person's roles and rules.
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=14, blank=True)
    street_address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=9, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=15, blank=True)
    longitude = models.CharField(max_length=15, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)

    class Meta:
        pass

    def age(self):
        """Returns person's age in years."""
        # TODO: check for a better algorithm
        today = datetime.date.today()
        # raised when birth date is February 29 and the current year is not a
        # leap year
        try:
            birthday = self.birth_date.replace(year=today.year)
        except ValueError:
            birthday = self.birth_date.replace(year=today.year,
                                               day=self.birth_date.day - 1)
        if birthday > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year

    def full_name(self):
        if self.middle_name:
            return "%s %s. %s" % (self.first_name, self.middle_name[0],
                                  self.last_name)
        else:
            return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name()


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
