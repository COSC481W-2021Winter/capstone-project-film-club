from django import template

import arrow

register = template.Library()

@register.simple_tag
def is_friend(user, profile):
    return user.userprofile.friends.filter(username = profile.username).exists()

@register.simple_tag
def get_normal_time(datetime):
    if datetime is None or len(datetime) == 0:
        return 'None'

    return arrow.get(datetime.replace('T', ' ').replace('Z', ' ').split('.')[0], 'YYYY-M-D HH:mm:ss').humanize()