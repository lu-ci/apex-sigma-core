import arrow


def make_move_log_embed(log_embed, guild):
    gld = guild
    creation_time = arrow.get(gld.created_at).format('DD. MMMM YYYY')
    bot_count = 0
    user_count = 0
    for user in gld.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    guild_text = f'Name: **{gld.name}**'
    guild_text += f'\nOwner: **{gld.owner.name}**#*{gld.owner.discriminator}*'
    guild_text += f'\nID: **{gld.id}**'
    guild_text += f'\nCreated: **{creation_time}**'
    nums_text = f'Members: **{user_count}**'
    nums_text += f'\nBots: **{bot_count}**'
    nums_text += f'\nChannels: **{len(gld.channels)}**'
    nums_text += f'\nRoles: **{len(gld.roles)}**'
    log_embed.add_field(name='Guild Info', value=guild_text)
    log_embed.add_field(name='Guild Stats', value=nums_text)
