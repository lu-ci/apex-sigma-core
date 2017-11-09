import asyncio

import discord

from .nodes.alert_functions import get_alert_data, generate_alert_embed
from .nodes.fissure_functions import get_fissure_data, generate_fissure_embed
from .nodes.invasion_functions import get_invasion_data, generate_invasion_embed
from .nodes.news_function import get_news_data, generate_news_embed
from .nodes.sortie_functions import get_sortie_data, generate_sortie_embed


# noinspection PyBroadException
async def wf_clockwork(ev):
    ev.bot.loop.create_task(wf_loop(ev))


async def wf_loop(ev):
    while True:
        try:
            await cycle_function(ev)
        except Exception:
            ev.log.error('The warframe clockwork couldn\'t complete a cycle.')
        await asyncio.sleep(5)


async def cycle_function(ev):
    all_guilds = ev.bot.guilds
    sorties = await get_sortie_data(ev.db)
    if sorties:
        sortie_response = generate_sortie_embed(sorties)
        for guild in all_guilds:
            sortie_channel = ev.db.get_guild_settings(guild.id, 'WarframeSortieChannel')
            if sortie_channel:
                sortie_target_channel = discord.utils.find(lambda x: x.id == sortie_channel, guild.channels)
                if sortie_target_channel:
                    try:
                        await sortie_target_channel.send(embed=sortie_response)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
    news = await get_news_data(ev.db)
    if news:
        news_response = generate_news_embed(news)
        for guild in all_guilds:
            news_channel = ev.db.get_guild_settings(guild.id, 'WarframeNewsChannel')
            if news_channel:
                news_target_channel = discord.utils.find(lambda x: x.id == news_channel, guild.channels)
                if news_target_channel:
                    try:
                        await news_target_channel.send(embed=news_response)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
    fissures = await get_fissure_data(ev.db)
    if fissures:
        fissure_response = generate_fissure_embed(fissures)
        for guild in all_guilds:
            fissure_channel = ev.db.get_guild_settings(guild.id, 'WarframeFissureChannel')
            if fissure_channel:
                fissure_target_channel = discord.utils.find(lambda x: x.id == fissure_channel, guild.channels)
                if fissure_target_channel:
                    try:
                        await fissure_target_channel.send(embed=fissure_response)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
    alerts, triggers = await get_alert_data(ev.db)
    if alerts:
        alert_response = await generate_alert_embed(alerts)
        for guild in all_guilds:
            mentions = []
            if triggers:
                for trigger in triggers:
                    wf_tags = ev.db.get_guild_settings(guild.id, 'WarframeTags')
                    if wf_tags is None:
                        wf_tags = {}
                    if wf_tags:
                        if trigger in wf_tags:
                            bound_role = discord.utils.find(lambda x: x.id == wf_tags[trigger], guild.roles)
                            if bound_role:
                                mentions.append(bound_role.mention)
            alert_channel = ev.db.get_guild_settings(guild.id, 'WarframeAlertChannel')
            if alert_channel:
                alert_target_channel = discord.utils.find(lambda x: x.id == alert_channel, guild.channels)
                if alert_target_channel:
                    try:
                        if mentions:
                            await alert_target_channel.send(' '.join(mentions), embed=alert_response)
                        else:
                            await alert_target_channel.send(embed=alert_response)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
    invasions, triggers = await get_invasion_data(ev.db)
    if invasions:
        invasion_response = await generate_invasion_embed(invasions)
        for guild in all_guilds:
            mentions = []
            if triggers:
                for trigger in triggers:
                    wf_tags = ev.db.get_guild_settings(guild.id, 'WarframeTags')
                    if wf_tags is None:
                        wf_tags = {}
                    if wf_tags:
                        if trigger in wf_tags:
                            bound_role = discord.utils.find(lambda x: x.id == wf_tags[trigger], guild.roles)
                            if bound_role:
                                mentions.append(bound_role.mention)
            invasion_channel = ev.db.get_guild_settings(guild.id, 'WarframeInvasionChannel')
            if invasion_channel:
                invasion_target_channel = discord.utils.find(lambda x: x.id == invasion_channel, guild.channels)
                if invasion_target_channel:
                    try:
                        if mentions:
                            await invasion_target_channel.send(' '.join(mentions), embed=invasion_response)
                        else:
                            await invasion_target_channel.send(embed=invasion_response)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
