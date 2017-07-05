def user_avatar(user):
    if user.avatar_url:
        output = user.avatar_url
    else:
        output = user.default_avatar_url
    return output


def movement_message_parser(member, text):
    guild = member.guild
    translator = {
        '{user_name}': member.name,
        '{user_mention}': member.mention,
        '{user_discriminator}': member.discriminator,
        '{user_id}': str(member.id),
        '{server_name}': guild.name,
        '{server_id}': str(guild.id),
        '{owner_name}': guild.owner.name,
        '{owner_mention}': guild.owner.mention,
        '{owner_discriminator}': guild.owner.discriminator,
        '{owner_id}': str(guild.owner.id)
    }
    greeting_text = text
    for key in translator:
        greeting_text = greeting_text.replace(key, translator[key])
    return greeting_text
