import discord
import re

from .mech.feh_core import FireEmblemHeroesCore

feh_core = None


async def fireemblemheroes(cmd, message, args):
    global feh_core
    if not feh_core:
        feh_core = FireEmblemHeroesCore(cmd.db)
    response = discord.Embed()
    if args:
        query = ' '.join(args).lower()
        query = re.sub(r'[1-9*]', '', query).strip()  # Strip numbers and asterisks from query
        record = feh_core.lookup(query)
        if record:
            if record['type'] == 'hero':
                response.set_author(name=f"{record['name']}: {record['title']}",
                                    url=record['url'],
                                    icon_url=feh_core.weapon_icons[record['color']][record['weapon type']])
                response.set_thumbnail(url=record['icon'])
                response.colour = feh_core.colors[record['color']]
                footer_text = f"{record['rarity']} | {record['color']} {record['weapon type']}"
                rarity = feh_core.get_specified_rarity(args[0])
                if not rarity:
                    response.description = record['bio']
                    for field in ['weapons', 'assists', 'specials', 'passives']:
                        if record[field]:
                            response.add_field(name=field.capitalize(), value=record[field], inline=False)
                else:
                    if rarity < 1 or rarity > 5 or rarity is False or str(rarity) not in record['stats'].keys():
                        # If specified rarity is not in 1-5⭐ range or not specified at all or doesn't exist
                        rarity = '5'
                    else:
                        rarity = str(rarity)
                    for stat_type in ['base', 'max']:
                        stats = record['stats'][rarity][stat_type]
                        stats = '\n'.join([f'**{key}**: {value}' for key, value in stats])
                        response.add_field(name=f'{rarity}\★ {stat_type} stats:', value=stats)
                    footer_text += ' | BST: ' + str(record['bst'][rarity])
                response.set_footer(icon_url=feh_core.move_icons[record['movement type']], text=footer_text)
            elif record['type'] == 'weapon':
                response.set_author(name=record['name'],
                                    url=record['url'],
                                    icon_url=feh_core.weapon_icons[record['color']][record['weapon type']])
                response.set_thumbnail(url=record['icon'])
                response.colour = feh_core.colors[record['color']]
                stats = {
                    'Might': record['might'],
                    'Range': record['range'],
                    'SP Cost': record['sp cost'],
                    "Exclusive": 'Yes' if record['exclusive'] else 'No'
                }
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]))
                if record['special effect']:
                    response.add_field(name='Special Effect', value=record['special effect'], inline=False)
                if record['heroes with']:
                    hero_list_title = f"List of heroes with {record['name']}"
                    response.add_field(name=hero_list_title, value=record['heroes with'], inline=False)
                if record['see also']:
                    response.set_footer(text=f"See also: {record['see also']}")
            elif record['type'] == 'assist':
                assist_icon = 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/9/9a/Icon_Skill_Assist.png'
                response.set_author(name=record['name'], url=record['url'], icon_url=assist_icon)
                response.colour = 0x05DEBB
                stats = {
                    'Range': record['range'],
                    'SP Cost': record['sp cost'],
                    "Inherit Restriction": record['inherit restriction']
                }
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]))
                response.add_field(name='Effect', value=record['effect'])
                response.add_field(name=f"List of heroes with {record['name']}", value=record['heroes with'])
            elif record['type'] == 'special':
                special_icon = 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/2/25/Icon_Skill_Special.png'
                response.set_author(name=record['name'], url=record['url'], icon_url=special_icon)
                response.colour = 0xE29DE7
                stats = {
                    'Cooldown': record['cooldown'],
                    'SP Cost': record['sp cost'],
                    "Inherit Restriction": record['inherit restriction']
                }
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]),
                                   inline=False)
                response.add_field(name='Effect', value=record['effect'], inline=False)
                response.add_field(name=f"List of heroes with {record['name']}", value=record['heroes with'])
            elif record['type'] == 'passive':
                icon = record['icon']
                response.set_author(name=record['name'], url=record['url'],
                                    icon_url=icon)
                response.set_thumbnail(url=icon)
                response.colour = feh_core.colors['Neutral']
                stats = {'Passive Type': record['passive type']}
                if record['passive type'] != 'S':
                    stats['SP Cost'] = record['sp cost']
                    stats['Inherit Restriction'] = record['inherit restriction']
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]),
                                   inline=False)
                response.add_field(name='Effect', value=record['effect'])
                if record['heroes with']:
                    response.add_field(name=f"List of heroes with {record['name']}", value=record['heroes with'])
                if record['see also']:
                    response.set_footer(text=f"See also: {record['see also']}")
        else:
            response.title = '🔍 No results.'
            response.colour = 0x696969
    else:
        response.title = '❗ Nothing inputted.'
        response.colour = 0xBE1931
    await message.channel.send(embed=response)
