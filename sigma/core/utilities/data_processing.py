def user_avatar(user):
    if user.avatar_url:
        output = user.avatar_url
    else:
        output = user.default_avatar_url
    return output
