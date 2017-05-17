from django.db import models
from django.core.urlresolvers import reverse
import datetime
from django.contrib.auth.models import User
import string


def get_letter(idx):

    alphabet = string.ascii_uppercase
    if idx < 25:
        return alphabet[idx]
    else:
        letter = ''
        letter += alphabet[int(idx / 26)-1]
        letter += alphabet[int(idx % 26)]
        return letter


def get_sample_name(sample_set_id):

    sampset = SampleSet.objects.get(pk=sample_set_id)
    base_name = sampset.set_name
    existing_codes = sampset.sample_set.all().order_by('-set_name')
    idx = existing_codes.count()

    return base_name + get_letter(idx)


def get_set_name():
    now = datetime.datetime.now()
    year = now.year
    letter = chr(year - 1952)
    existing_names = SampleSet.objects.all().order_by('-set_name')
    new_number = 1
    if existing_names.count() > 0:
        initial_letter = existing_names[0].set_name[0]
        if initial_letter == letter:
            new_number = int(existing_names[0].set_name[1:]) + 1

    return letter + '%03d' % new_number


class Institute(models.Model):

    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Client(models.Model):

    name = models.CharField(max_length=1000)
    institute = models.ForeignKey(Institute, null=True)

    def __str__(self):
        return self.name


class SampleSet(models.Model):

    set_name = models.CharField(max_length=250, editable=False, default=get_set_name)
    number_of_samples = models.PositiveSmallIntegerField(default=0, editable=False)
    samples_set_description = models.CharField(max_length=2000)
    registration_date = models.DateTimeField(auto_now_add=True)
    final_report = models.FileField(null=True, blank=True)
    client = models.ForeignKey(Client, null=True)
    registered_by = models.ForeignKey(User, null=True)

    def get_absolute_url(self):
        return reverse('sample:detail', kwargs={'sampleset_id': self.pk})

    def __str__(self):
        return self.set_name


class Sample(models.Model):

    sample_set = models.ForeignKey(SampleSet, on_delete=models.CASCADE)
    sample_code = models.CharField(max_length=250, editable=False)
    sample_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.sample_code + ' (' + self.sample_set.set_name + ')'
