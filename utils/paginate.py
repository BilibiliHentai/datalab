from django.core.paginator import Paginator


def paginate(data, current_page, itemsum_of_page):
    paginator = Paginator(data, itemsum_of_page)
    page = current_page
    if page < 1:
        page = 1
    elif page > paginator.num_pages:
        page = paginator.num_pages

    return {
        'num_pages': paginator.num_pages,
        'page': page,
        'next_page': page + 1,
        'prev_page': page if page == 1 else page - 1,
    }
