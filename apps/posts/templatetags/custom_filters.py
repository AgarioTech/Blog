import re
from django import template
from django.utils import timezone
from django.utils.formats import date_format

register = template.Library()

@register.filter
def smart_time(datetime):
    now = timezone.localtime(datetime)
    result = timezone.now() - datetime
    seconds = int(result.total_seconds())
    minutes = seconds // 60
    hours = seconds // 3600


    if result.days > 0:
        return date_format(now, format="H:i", use_l10n=True)



    if hours > 0:
        return f"{hours} ч назад"
    else:
        if minutes < 1:
            return f"{seconds} с назад"
        else:
            return f"{minutes} мин назад" 
        
@register.filter
def split_content(value):
    paragraphs = value.split('</p>')
    first = paragraphs[0] + '</p>'
    text = re.sub(r'<.*?>', '', first)
    if len(text) <= 300:
        return paragraphs[0] + '</p>'
    else:
        return ''

