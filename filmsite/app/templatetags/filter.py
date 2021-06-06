from django import template
register = template.Library()


@register.filter
def g(h, key):
    return h.get(key, 'null')


@register.filter
def tf(h):
    return h[0]


@register.filter
def ts(h):
    return h[1]


@register.filter
def sub(h, key):
    return h-key


@register.filter
def first(h):
    return [h.first()]


@register.filter
def none_str(h):
    return h if h else '---'


@register.filter
def skip_first(h):
    return h[1:]


@register.filter
def len(h):
    return h.__len__()


@register.filter
def noneStr(h):
    return h if h else ''


@register.filter
def no_id(h):
    return h if h else 0


@register.filter
def get_rate(h, id):
    if h == '':
        return '/'
    query = h.filter(user__id=id)
    
    if query.__len__() > 0:
        if query.get().rate:
            return query.get().rate 

    return '/'

@register.filter
def get_contents(h, id):
    if h == '':
        return '/'
    query = h.filter(user__id=id)
    
    if query.__len__() > 0:
        if query.get().contents:
            return query.get().contents 

    return '/'

@register.filter
def get(h, key):
    if key:
        return getattr(h.get(), key) if getattr(h.get(), key) else '/'
    else:
        return h.get()

@register.filter
def get_f(f, key):
    return getattr(f, key)
