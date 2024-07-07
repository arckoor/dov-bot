from dataclasses import dataclass


@dataclass
class Guild:
    id: int = 0
    name: str = ""


@dataclass
class Role:
    id: int = 0
    name: str = ""
    mention: str = ""
    guild: Guild = None


def get_alternate_role(id: int = None, name: str = None, mention: str = None, guild: dict = None) -> Role:
    id = coalesce(id, 0)
    name = coalesce(name, "Unknown")
    mention = coalesce(mention, "<@Unknown>")
    if not guild:
        guild = Guild(id=0, name="Unknown")
    else:
        guild = Guild(**guild)
    return Role(id=id, name=name, mention=mention, guild=guild)


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
