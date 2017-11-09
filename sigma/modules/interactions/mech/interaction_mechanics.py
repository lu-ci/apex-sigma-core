import secrets

import discord

interaction_cache = {}


def grab_interaction(db, intername):
    if intername not in interaction_cache:
        fill = True
    else:
        if not interaction_cache[intername]:
            fill = True
        else:
            fill = False
    if fill:
        interactions = db[db.db_cfg.database]['Interactions'].find({'Name': intername})
        interactions = list(interactions)
        interaction_cache.update({intername: interactions})
    if interaction_cache[intername]:
        choice = interaction_cache[intername].pop(secrets.randbelow(len(interaction_cache[intername])))
    else:
        choice = {'URL': 'https://i.imgur.com/m59E4nx.gif', 'UserID': None, 'ServerID': None}
    return choice


def get_target(message):
    if message.mentions:
        target = message.mentions[0]
    else:
        if message.content:
            lookup = ' '.join(message.content.split(' ')[1:])
            target = discord.utils.find(
                lambda x: x.display_name.lower() == lookup.lower() or x.name.lower() == lookup.lower(),
                message.guild.members)
        else:
            target = None
    return target


def make_footer(cmd, item):
    if item['UserID']:
        uid = item['UserID']
        user = discord.utils.find(lambda x: x.id == uid, cmd.bot.get_all_members())
        if user:
            username = user.name
        else:
            username = 'Unknown User'
    else:
        username = 'Unknown User'
    sid = item['ServerID']
    srv = discord.utils.find(lambda x: x.id == sid, cmd.bot.guilds)
    if srv:
        servername = srv.name
    else:
        servername = 'Unknown Server'
    footer = f'Submitted by {username} from {servername}.'
    return footer
