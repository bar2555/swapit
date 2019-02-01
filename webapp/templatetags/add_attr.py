from django import template
register = template.Library()

''' helper function to allow css attributes to be added to form fields
in django's template language more easily'''
@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})

''' helper function to add attributes to form fields
credit https://blog.joeymasip.com/'''
@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return field.as_widget(attrs=attrs)
