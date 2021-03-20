from django import template

import arrow

register = template.Library()

colors = [('#41a749', 5), ('#70b73a', 4), ('#d8d21c', 3), ('#d27635', 2), ('#a74141', 1), ('#a74141', 0)]

@register.simple_tag
def is_friend(user, profile):
    return user.userprofile.friends.filter(username = profile.username).exists()

@register.simple_tag
def get_normal_time(datetime):
    if datetime is None or len(datetime) == 0:
        return 'None'

    return arrow.get(datetime.replace('T', ' ').replace('Z', ' ').split('.')[0], 'YYYY-M-D HH:mm:ss').humanize()

@register.simple_tag
def get_review_color(score):
    if score == '' or score is None:
        return ''

    try:
        score = int(score)

        for color_pair in colors:
            if score >= color_pair[1]:
                return color_pair[0]
    except:
        pass

    return '#aaa'