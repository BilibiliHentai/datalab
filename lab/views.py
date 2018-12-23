from collections import Counter, OrderedDict
from django.http import JsonResponse
from django.shortcuts import render
import copy

from utils.read_json_data import JsonReader
from utils.read_xml_data import XmlReader

JSON_READER = JsonReader()
JSON_READER.read()
XML_READER = XmlReader()
XML_READER.read()


def index(request):
    total_numbers = JSON_READER.get_total_number()
    data = JSON_READER.get_score_sorted_data()
    context = {
        'subtemplate': 'lab/main.html',
        'data': data,
        'gene_sum': total_numbers['total_gene_number'],
        'compound_sum': total_numbers['total_compound_number'],
        'related_publication_sum': total_numbers['total_related_publication'],
    }
    return render(request, 'lab/index.html', context=context)


def statistics(request):
    total_numbers = JSON_READER.get_total_number()
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
    genes = XML_READER.get_genes()
    gene = genes.get(gene_id, None)
    context = {
        'subtemplate': 'lab/gene-detail.html',
        'gene': gene
    }
    return render(request, 'lab/index.html', context=context)


def compound(request, category=None):
    categories = set()
    [categories.add(j) for i in XML_READER.get_drugs() for j in i['categories']]
    context = {
        'subtemplate': 'lab/compound.html',
        'categories': sorted(categories),

    }
    return render(request, 'lab/index.html', context=context)


def compound_detail(request, compound_id):
    compound = None
    for i in XML_READER.get_drugs():
        if i['drugbank_id'] == compound_id:
            compound = i

    context = {
        'subtemplate': 'lab/compound-detail.html',
        'compound': compound,
        'range': range(10)
    }
    return render(request, 'lab/index.html', context=context)


def help(request):
    context = {'subtemplate': 'lab/help.html'}
    return render(request, 'lab/index.html', context=context)


def sortdata(data, reverse: bool = True) -> list:
    return sorted(data, key=lambda x: x['score'], reverse=reverse)


def get_score_frequency(request):
    scores = JSON_READER.get_all_score()
    scores.sort()
    temp_scores = copy.deepcopy(scores)
    for i, v in enumerate(temp_scores):
        scores[i] = round(v, 2)
    scores_frequency = OrderedCounter()
    for i in scores:
        scores_frequency[i] += 1
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


def get_gene_by_name(request, gene_name):
    rows = []
    for k, v in XML_READER.get_genes().items():
        if gene_name == v['name']:
            rows.append(v)
    return JsonResponse({'data': rows})


def get_compound_by_category(request, category):
    data = XML_READER.get_drugs()  # a list of dict
    rows = []
    if category is not None:
        for datum in data:
            if category in datum['categories']:
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
    data = XML_READER.get_drugs()
    for datum in data:
        if datum['drugbank_id'] == compound_id:
            return JsonResponse({
                'targets': datum['targets']
            })
    return JsonResponse({'targets': None})


def get_associated_targets(request, compound_id):
    data = JSON_READER.get_data()
    for datum in data:
        if compound_id == datum['drug_id']:
            return JsonResponse({
                'targets': [x['target'] for x in datum['supporting_entry']],
                'score': datum['predict_score'],
                'supported_entries': datum['supporting_entry']
            })
    return JsonResponse(None)


def get_associated_compounds(request, gene_id):
    gene = XML_READER.get_genes()[gene_id]
    compounds = gene['compounds']
    useful_compounds = []
    for compound in compounds:
        for datum in JSON_READER.get_data():
            if datum['drug_id'] == compound['drugbank_id']:
                compound['target_id'] = datum['target_id']
                compound['score'] = datum['predict_score']
                compound['supported_entries'] = datum['supporting_entry']
                useful_compounds.append(copy.deepcopy(compound))
    return JsonResponse({
        'compounds': useful_compounds
    })


def get_supported_entries_by_target_id(request, target_id):
    for datum in JSON_READER.get_data():
        if datum['target_id'] == target_id:
            print(datum['supporting_entry'])
            return JsonResponse({'supported_entries': datum['supporting_entry']})
    return JsonResponse({'': ''})


# a python recipe
class OrderedCounter(Counter, OrderedDict):
    """Counter that remembers the order elements are first encountered"""

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)
