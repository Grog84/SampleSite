from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import SampleSet, Sample, Client
from django.forms.models import model_to_dict
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render_to_response
import string

sets_table_head_list = ['#', 'Set Name', 'Samples Nbr.', 'Description', 'Date', 'Client']
samples_head_list = ['#', 'Code', 'Description']


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

    sampset = get_list_or_404(SampleSet, pk=sample_set_id)
    base_name = sampset[0].set_name
    existing_codes = sampset[0].sample_set.all().order_by('-set_name')
    idx = existing_codes.count()

    return base_name + get_letter(idx)


def to_dict(instance):

    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data


@login_required
def index(request):
    return render_to_response('sample/index.html', {'user': request.user})


@login_required
def sets(request):

    all_samples_set = SampleSet.objects.all()

    # table_values_list = [f.name for f in SampleSet._meta.get_fields()][1:]
    # table_head_list = ['#', 'Set Name', 'Samples Nbr.', 'Description', 'Date']

    table = list()
    for sam in all_samples_set:
        sam_dict = to_dict(sam)
        sam_dict.pop('final_report', None)

        client = get_object_or_404(Client, pk=sam_dict['client'])
        sam_dict['client'] = client.name

        table.append(sam_dict)

    context = {
        'all_samples_set': all_samples_set,
        'table_head_list': sets_table_head_list,
        'table': table,
        'link_key': 'set_name',
        'link_url_name': 'sample:set_detail',
    }
    return render(request, 'sample/sets.html', context)


@login_required
def samples(request):

    table = list()
    all_samples = list()
    all_samples_set = SampleSet.objects.all()
    for sampset in all_samples_set:
        set_samples = sampset.sample_set.all()
        if len(set_samples) is not 0:
            all_samples.append(set_samples)
            for sam in set_samples:
                sam_dict = model_to_dict(sam)
                sam_dict.pop('sample_set', None)
                table.append(sam_dict)

    context = {
        'all_samples': all_samples,
        'table_head_list': samples_head_list,
        'table': table,
        'link_key': 'sample_code',
        'link_url_name': 'sample:sample_detail',
    }
    return render(request, 'sample/samples.html', context)


@login_required
def set_detail(request, sampleset_id):

    sampset = get_list_or_404(SampleSet, pk=sampleset_id)
    sampset_dict = to_dict(sampset[0])
    sampset_dict.pop('final_report', None)
    client = get_object_or_404(Client, pk=sampset_dict['client'])
    sampset_dict['client'] = client.name

    new_sampset_dict = dict()
    for ii, key in enumerate(sampset_dict.keys()):
        new_sampset_dict[sets_table_head_list[ii]] = sampset_dict[key]

    all_samples = sampset[0].sample_set.all()
    samples_head_list = ['#', 'Code', 'Description']

    table = []
    for sam in all_samples:
        sam_dict = model_to_dict(sam)
        sam_dict.pop('sample_set', None)
        table.append(sam_dict)

    context = {
        'sampset': sampset,
        'sampset_dict': new_sampset_dict,
        'table_head_list': samples_head_list,
        'table': table,
        'link_key': 'sample_name',
        'link_url_name': 'sample:sample_detail',
    }

    return render(request, 'sample/set_detail.html', context)


@login_required
def sample_detail(request, sample_id):

        sample = get_list_or_404(Sample, pk=sample_id)
        sample_dict = to_dict(sample[0])

        new_sample_dict = dict()
        keys = list(sample_dict.keys())
        keys.remove('sample_set')
        for ii, key in enumerate(keys):
            new_sample_dict[samples_head_list[ii]] = sample_dict[key]

        context = {
            'sample': sample,
            'sample_dict': new_sample_dict,
        }

        return render(request, 'sample/sample_detail.html', context)


class LogoutView(RedirectView):

    login_required = True
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SampleSetCreate(CreateView):
    login_required = True
    model = SampleSet
    fields = ['set_name', 'number_of_samples', 'samples_set_description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(SampleSetCreate, self).form_valid(form)


class SampleSetUpdate(UpdateView):
    login_required = True
    model = SampleSet
    fields = ['set_name', 'number_of_samples', 'samples_set_description']


class SampleSetDelete(DeleteView):
    login_required = True
    model = SampleSet
    success_url = reverse_lazy('sample:index')


# from django.views import generic
# from .models import SampleSet
#
# class IndexView(generic.ListView):
#
#     template_name = 'sample/index.html'
#     context_object_name = 'all_samples_set'
#
#     def get_queryset(self):
#         return SampleSet.objects.all()
#
#
# class DetailView(generic.DetailView):
#
#     model = SampleSet
#     template_name = 'sample/detail.html'


class SampleCreate(CreateView):

    login_required = True
    model = Sample
    fields = ['sample_description']