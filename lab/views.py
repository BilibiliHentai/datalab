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


# def get_drugs(request, keyword='rivaroxaban', page=1):
#     """all data will be returned by search, \n
#     if not given, there's a default keyword.
#
#     Arguments:
#         request {} -- none
#
#     Keyword Arguments:
#         keyword {str} -- [name of gene or compound] (default: {'rivaroxaban'})
#         page {int} -- [for pagination] (default: {1})
#
#     Returns:
#         [HttpResponse] -- none
#     """
#
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword', 'rivaroxaban')
#         page = int(request.POST.get('page', 1))
#     test_data_set = TestData()
#
#     if settings.DEBUG is True:
#         # test data for development
#         data = test_data_set.get_test_data(keyword)
#     else:
#         # real data for production
#         data = search(keyword, True)
#         database.close()
#
#     paginator = Paginator(data, 10)
#     if page < 1:
#         page = 1
#     elif page > paginator.num_pages:
#         page = paginator.num_pages
#     context = {
#         'data': paginator.get_page(page),
#         'keyword': keyword,
#         'num_pages': paginator.num_pages,
#         'page': page,
#         'next_page': page + 1,
#         'prev_page': page if page == 1 else page - 1,
#         'subtemplate': 'lab/drugs.html',
#     }
#     return render(request, 'lab/index.html', context=context)


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
    # if gene_name is None:
    #     gene_name = 'prothrombinase'
    # else:
    #     gene_name = 'prothrombinase'
    #     data = database.query_gene(gene_name)
    #     protein_name = 'protein'
    #     categories = 'categories'
    #     associate_compound_sum = len(data)
    context = {
        'subtemplate': 'lab/gene.html',
        'gene_name': 'www',
        # 'categories': categories,
        # 'protein_name': protein_name,
        # 'associate_compound_sum': associate_compound_sum,
    }
    return render(request, 'lab/index.html', context=context)


def gene_detail(request, gene_name):
    context = {
        'subtemplate': 'lab/gene-detail.html',
    }
    return render(request, 'lab/index.html', context=context)


def compound(request, category=None):
    categories = set()
    [categories.add(j) for i in XML_READER.get_data() for j in i['categories']]
    context = {
        'subtemplate': 'lab/compound.html',
        'categories': sorted(categories),

    }
    return render(request, 'lab/index.html', context=context)


def compound_detail(request, compound_id):
    for i in XML_READER.get_data():
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
    for datum in XML_READER.get_data():
        if compound_name == datum['drug_name']:
            rows.append({
                'id': datum['drugbank_id'],
                'name': datum['drug_name'],
                'categories': datum['categories'],
                'associate_gene_number': len(datum['targets'])
            })
    return JsonResponse({'data': rows})


def get_compound_by_category(request, category):
    data = XML_READER.get_data()  # a list of dict
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
    data = XML_READER.get_data()
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
            print(datum)
            return JsonResponse({
                'targets': [x['target'] for x in datum['supporting_entry']],
                'score': datum['predict_score'],
                'supported_entries': datum['supporting_entry']
            })
    return JsonResponse(None)


# a python recipe
class OrderedCounter(Counter, OrderedDict):
    """Counter that remembers the order elements are first encountered"""

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)
