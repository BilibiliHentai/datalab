from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from data_lab import settings

if settings.DEBUG is True:
    from .TestData import TestData
else:
    from lab.mongo_db import database


def index(request):
    context = {
        'subtemplate': 'lab/main.html',
    }
    return render(request, 'lab/index.html', context=context)


def get_drugs(request, keyword='rivaroxaban', page=1):
    """all data will be returned by search, \n
    if not given, there's a default keyword.

    Arguments:
        request {} -- none

    Keyword Arguments:
        keyword {str} -- [name of gene or compound] (default: {'rivaroxaban'})
        page {int} -- [for pagination] (default: {1})

    Returns:
        [HttpResponse] -- none
    """

    if request.method == 'POST':
        keyword = request.POST.get('keyword', 'rivaroxaban')
        page = int(request.POST.get('page', 1))
    test_data_set = TestData()

    if settings.DEBUG is True:
        # test data for development
        data = test_data_set.get_test_data(keyword)
    else:
        # real data for production
        data = search(keyword, True)
        database.close()

    paginator = Paginator(data, 10)
    if page < 1:
        page = 1
    elif page > paginator.num_pages:
        page = paginator.num_pages
    context = {
        'data': paginator.get_page(page),
        'keyword': keyword,
        'num_pages': paginator.num_pages,
        'page': page,
        'next_page': page+1,
        'prev_page': page if page == 1 else page - 1,
        'subtemplate': 'lab/drugs.html',
    }
    return render(request, 'lab/index.html', context=context)


def statistics(request):
    context = {'subtemplate': 'lab/statistics.html'}
    return render(request, 'lab/index.html', context=context)


def gene(request):
    context = {
        'gene_name': 'prothrombinase',
        'subtemplate': 'lab/gene.html',
    }
    return render(request, 'lab/index.html', context=context)


def gene_detail(request, gene_name):
    context = {'subtemplate': 'lab/gene-detail.html'}
    return render(request, 'lab/index.html', context=context)


def compound(request):
    context = {
        'compound_name': 'rivaroxaban',
        'subtemplate': 'lab/compound.html'
    }
    return render(request, 'lab/index.html', context=context)


def compound_detail(request, compound_name):
    context = {'subtemplate': 'lab/compound-detail.html'}
    return render(request, 'lab/index.html', context=context)


def help(request):
    context = {'subtemplate': 'lab/help.html'}
    return render(request, 'lab/index.html', context=context)


def search(keyword: str, set_sort: bool = True) -> list:
    data = database.query_gene(keyword)
    if not data:
        data = database.query_compound(keyword)
    return sorted(data, key=lambda x: x['cite_num'], reverse=True)
