from django import template

register = template.Library()

@register.simple_tag
def is_friend(user, profile):
    return user.userprofile.friends.filter(username = profile.username).exists()