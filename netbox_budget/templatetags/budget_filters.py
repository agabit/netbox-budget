from django import template

register = template.Library()


@register.filter
def format_kzt(value):
    """Format number as readable KZT: 11 854 560 KZT"""
    try:
        value = float(value)
        formatted = f"{abs(value):,.0f}".replace(',', ' ')
        return f"{formatted} KZT"
    except (ValueError, TypeError):
        return value


@register.filter
def format_kzt_signed(value):
    """Format number with + or - sign and white text: +11 854 560 KZT or -11 854 560 KZT"""
    try:
        value = float(value)
        formatted = f"{abs(value):,.0f}".replace(',', ' ')
        if value > 0:
            return f"-{formatted} KZT"
        elif value < 0:
            return f"+{formatted} KZT"
        else:
            return f"0 KZT"
    except (ValueError, TypeError):
        return value
