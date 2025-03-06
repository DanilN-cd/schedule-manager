from django import template
import datetime
from testapp.models import Predmets

register = template.Library()

@register.filter
def add_days(date, days):
    return date + datetime.timedelta(days=days)

@register.filter
def get_entry(days, date):
    return days.get(date, [])

@register.simple_tag
def get_pair_and_group(entries, pair_number, group):
    """
    Тег, который ищет запись для конкретной пары и группы.
    """
    for entry in entries:
        if entry.pair_number == pair_number and entry.group == group:
            return entry
    return None

@register.filter
def subjects_for_group(group):
    return Predmets.objects.filter(group=group)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)