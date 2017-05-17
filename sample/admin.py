from django.contrib import admin
from .models import SampleSet, Sample, Client, Institute

admin.site.register(SampleSet)
admin.site.register(Sample)
admin.site.register(Client)
admin.site.register(Institute)