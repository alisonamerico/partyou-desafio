from django.template import Library

register = Library()


@register.inclusion_tag('pagination.html')
def pagination(request, paginator, page_obj):
    context = {}
    context['paginator'] = paginator
    context['request'] = request
    context['page_obj'] = page_obj
    getvars = request.GET.copy()
    if 'page' in getvars:
        del getvars['page']  # pragma: no cover
    if len(getvars) > 0:
        context['getvars'] = '&{0}'.format(getvars.urlencode())  # pragma: no cover
    else:
        context['getvars'] = ''
    return context
