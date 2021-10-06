from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user

    if context.request.user.is_anonymous:
        return None
    else:
        the_list = list_models.List.objects.get_or_none(
            user=user, name="My Favourites Houses"
        )

        # the original code starts
        if the_list == None:
            return 0
        else:
            return room in the_list.rooms.all()
        # the original code ends
