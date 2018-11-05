from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from data_lab import settings

if settings.DEBUG is True:
    from .TestData import TestData
else:
    from lab.mongo_db import database


def index(request, keyword='rivaroxaban', page=1):
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
    print(type(page))
    if page < 1:
        page = 1
    elif page > paginator.num_pages:
        page = paginator.num_pages
    context = {
        'data': paginator.get_page(page),
        'keyword': keyword,
        'num_pages': paginator.num_pages,
        'page': page,
    }
    return render(request, 'lab/semanticwb.html', context=context)


def statistics(request):
    return render(request, 'lab/statistics.html')


def search(keyword: str, set_sort: bool = True) -> list:
    data = database.query_gene(keyword)
    if not data:
        data = database.query_compound(keyword)
    database.close()
    return sorted(data, key=lambda x: x['cite_num'], reverse=True)
