from collections import Counter, OrderedDict
from django.http import JsonResponse
from django.shortcuts import render
import copy

from utils.read_json_data import JsonReader
from utils.read_xml_data import XmlReader
from .mongo_models import DB

JSON_READER = JsonReader()
JSON_READER.read()
XML_READER = XmlReader()
XML_READER.read()
db = DB()


def index(request):
    # total_numbers = JSON_READER.get_total_number()
    # data = JSON_READER.get_score_sorted_data()
    total_numbers = db.get_total_number()
    data = db.get_score_sorted_data()
    context = {
        'subtemplate': 'lab/main.html',
        'data': data,
        'gene_sum': total_numbers['total_gene_number'],
        'compound_sum': total_numbers['total_compound_number'],
        'related_publication_sum': total_numbers['total_related_publication'],
    }
    return render(request, 'lab/index.html', context=context)


def statistics(request):
    total_numbers = db.get_total_number()
    context = {
        'subtemplate': 'lab/statistics.html',
        'gene_sum': total_numbers['total_gene_number'],
        'compound_sum': total_numbers['total_compound_number'],
        'related_publication_sum': total_numbers['total_related_publication'],
    }
    return render(request, 'lab/index.html', context=context)


def gene(request):
    context = {
        'subtemplate': 'lab/gene.html',
    }
    return render(request, 'lab/index.html', context=context)


def gene_detail(request, gene_id):
    gene = db.get_gene_by_id(gene_id)
    context = {
        'subtemplate': 'lab/gene-detail.html',
        'gene': gene
    }
    return render(request, 'lab/index.html', context=context)


def compound(request, category=None):
    categories = db.get_compound_categories()
    context = {
        'subtemplate': 'lab/compound.html',
        'categories': sorted(categories),

    }
    return render(request, 'lab/index.html', context=context)


def compound_detail(request, compound_id):
    compound = db.get_compound_by_drugbank_id(compound_id)
    context = {
        'subtemplate': 'lab/compound-detail.html',
        'compound': compound
    }
    return render(request, 'lab/index.html', context=context)


def help(request):
    context = {'subtemplate': 'lab/help.html'}
    return render(request, 'lab/index.html', context=context)


def get_score_frequency(request):
    scores_frequency = db.get_score_frequency()
    return JsonResponse(scores_frequency)


def get_compound_by_name(request, compound_name):
    rows = []
    for datum in XML_READER.get_drugs():
        if compound_name == datum['drug_name']:
            rows.append({
                'id': datum['drugbank_id'],
                'name': datum['drug_name'],
                'categories': datum['categories'],
                'associate_gene_number': len(datum['targets'])
            })
    return JsonResponse({'data': rows})


def get_genes_by_name(request, gene_name):
    genes = db.get_genes_by_name(gene_name)
    return JsonResponse({'data': genes})


def get_compound_by_category(request, category):
    data = db.get_compounds_by_category(category)  # a list of dict
    rows = []
    if category is not None:
        for datum in data:
            row = {
                'id': datum['drugbank_id'],
                'name': datum['drug_name'],
                'categories': datum['categories'],
                'associate_gene_number': len(datum['targets'])
            }
            rows.append(row)
    return JsonResponse({'data': rows})


def get_known_targets(request, compound_id):
    """
    for dti known targets
    :param request:
    :param compound_id:
    :return: JsonResponse
    """
    data = db.get_known_targets(compound_id)
    # for datum in data:
    #     if datum['drugbank_id'] == compound_id:
    #         return JsonResponse({
    #             'targets': datum['targets']
    #         })
    return JsonResponse({'targets': data})


def get_associated_targets(request, compound_id):
    targets = db.get_associated_targets(compound_id)
    print(targets)
    return JsonResponse({'targets': targets})


def get_associated_compounds(request, gene_id):
    compounds = db.get_associated_compounds(gene_id)
    return JsonResponse({'compounds': compounds})


def get_supported_entries_by_ids(request, target_id, drug_id):
    supported_entries = db.get_supported_entries_by_ids(target_id, drug_id)
    return JsonResponse(supported_entries)


def get_supported_entries_by_drug_id(request, drug_id):
    supported_entries = db.get_supported_entries_by_drug_id(drug_id)
    return JsonResponse(supported_entries)


# a python recipe
class OrderedCounter(Counter, OrderedDict):
    """Counter that remembers the order elements are first encountered"""

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)
