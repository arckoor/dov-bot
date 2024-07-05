# https://stackoverflow.com/a/16247152/12203337
def coalesce(*args):
    return next((a for a in args if a is not None), None)


def time_to_text(t1: float, t2: float):
    diff = t2 - t1
    days, remainder = divmod(diff, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    formatted = ""
    if days:
        formatted += f"{days:.0f} day{'s' if days > 1 else ''}, "
    if hours or days:
        formatted += f"{hours:02.0f} hour{'s' if hours > 1 else ''}, "
    if minutes or not (days or hours):
        formatted += f"{minutes:02.0f} minute{'s' if minutes > 1 else ''}"

    return formatted
