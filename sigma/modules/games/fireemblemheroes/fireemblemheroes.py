import discord

from .mech.feh_core import FireEmblemHeroesCore

feh_core = None


async def fireemblemheroes(cmd: SigmaCommand, message: discord.Message, args: list):
    global feh_core
    if not feh_core:
        feh_core = FireEmblemHeroesCore(cmd.db)
        await feh_core.init_index()
    response = discord.Embed()
    if not args:
        response.title = '❗ Nothing inputted.'
        response.colour = 0xBE1931
    else:
        query = ' '.join(args).lower()
        record = await feh_core.lookup(query)
        if not record:
            response.title = '🔍 No results.'
            response.colour = 0x696969
        else:
            record_type = record['type']
            author_name = record['name']

            if record_type in ['hero', 'weapon']:
                author_icon = feh_core.weapon_icons[record['color']][record['weapon type']]
                response_colour = feh_core.colors[record['color']]

            if record_type == 'hero':
                author_name += f": {record['title']}"
                footer_text = f"{record['rarity']} | {record['color']} {record['weapon type']}"
                rarity = feh_core.get_specified_rarity(args[0])
                if not rarity:
                    # Rarity not specified, respond with hero bio if available and hero skills
                    if record['bio']:
                        response.description = record['bio']
                    for field in ['weapons', 'assists', 'specials', 'passives']:
                        if record[field]:
                            response.add_field(name=field.capitalize(), value=record[field], inline=False)
                else:
                    # Rarity is specified, respond with stats for specified rarity
                    if rarity < 1 or rarity > 5 or rarity is False or str(rarity) not in record['stats'].keys():
                        # If specified rarity is not in 1-5⭐ range or not specified at all or doesn't exist
                        # Default to 5⭐
                        rarity = '5'
                    else:
                        rarity = str(rarity)
                    for stat_type in ['base', 'max']:
                        stats = record['stats'][rarity][stat_type]
                        stats = '\n'.join([f'**{key}**: {value}' for key, value in stats])
                        response.add_field(name=f'{rarity}\★ {stat_type} stats:', value=stats)
                    footer_text += ' | BST: ' + str(record['bst'][rarity])
                response.set_footer(icon_url=feh_core.move_icons[record['movement type']], text=footer_text)
            elif record_type == 'weapon':
                stats = [f"Might {record['might']}", f"Range {record['range']}", f"SP {record['sp cost']}"]
                if record['exclusive']:
                    stats.append('Is exclusive')
                response.add_field(name='Stats', value=', '.join(stats), inline=False)
                if record['special effect']:
                    response.add_field(name='Effect', value=record['special effect'], inline=False)
                if record['evolution']:
                    response.add_field(name='Evolves into',
                                       value=f"{record['evolution']['into']} ({record['evolution']['cost']})")
                if record['upgrade effect']:
                    response.add_field(name='Upgraded effect', value=record['upgrade effect'], inline=False)
                if record['upgrades']:
                    upgrades = ''
                    for upgrade_type in ['passive', 'stat']:
                        if record['upgrades'][upgrade_type]:
                            upgrades = f"| " + '\n| '.join(record['upgrades'][upgrade_type])
                    if upgrades:
                        response.add_field(name='Upgrades', value=upgrades, inline=False)
                    if record['upgrades']['cost']:
                        response.add_field(name='Upgrade cost', value=record['upgrades']['cost'], inline=False)
            elif record_type == 'assist':
                author_icon = 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/9/9a/Icon_Skill_Assist.png'
                response_colour = 0x05DEBB
                stats = [f"Range {record['range']}", f"SP {record['sp cost']}"]
                if record['inherit restriction']:
                    stats.append(record['inherit restriction'])
                response.add_field(name='Stats', value=', '.join(stats))
                response.add_field(name='Effect', value=record['effect'])
            elif record_type == 'special':
                author_icon = 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/2/25/Icon_Skill_Special.png'
                response_colour = 0xE29DE7
                stats = [f"Cooldown {record['cooldown']}", f"SP {record['sp cost']}"]
                if record['inherit restriction']:
                    stats.append(record['inherit restriction'])
                response.add_field(name='Stats', value=', '.join(stats), inline=False)
                response.add_field(name='Effect', value=record['effect'], inline=False)
            elif record_type == 'passive':
                author_icon = record['icon']
                response_colour = feh_core.colors['Neutral']
                stats = [f"Passive type {record['passive type']}"]
                if record['passive type'] != 'S':
                    stats.append(f"SP {record['sp cost']}")
                if record['inherit restriction']:
                    stats.append(record['inherit restriction'])
                response.add_field(name='Stats', value=', '.join(stats), inline=False)
                response.add_field(name='Effect', value=record['effect'])

            response.set_author(name=author_name, url=record['url'], icon_url=author_icon)
            response.colour = response_colour
            if record_type not in ['assist', 'special']:
                if record['icon']:
                    response.set_thumbnail(url=record['icon'])

            if record_type not in ['hero']:
                if record['heroes with']:
                    response.add_field(name=f"List of heroes with {record['name']}",
                                       value=record['heroes with'],
                                       inline=False)
    await message.channel.send(embed=response)
