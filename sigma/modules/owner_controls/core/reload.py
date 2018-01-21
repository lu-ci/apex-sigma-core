from sigma.core.mechanics.command import SigmaCommand
from importlib import reload as reimport
from sigma.modules.development.version_updater import version_updater
import discord


async def reload(cmd: SigmaCommand, message: discord.Message, args: list):
    await version_updater(cmd)
    if not args:
        cmd.log.info('---------------------------------')
        cmd.log.info('Reloading all modules...')
        cmd.bot.ready = False
        response = discord.Embed(color=0xF9F9F9, title='⚗ Reloading all modules...')
        load_status = await message.channel.send(embed=response)
        cmd.bot.init_modules()
        cmd_count = len(cmd.bot.modules.commands)
        ev_count = 0
        for key in cmd.bot.modules.events:
            event_group = cmd.bot.modules.events[key]
            ev_count += len(event_group)
        load_end_title = f'✅ Loaded {cmd_count} Commands and {ev_count} Events.'
        load_done_response = discord.Embed(color=0x77B255, title=load_end_title)
        await load_status.edit(embed=load_done_response)
        cmd.bot.ready = True
        cmd.log.info(f'Loaded {cmd_count} commands and {ev_count} events.')
        cmd.log.info('---------------------------------')
    else:
        command_name = ' '.join(args)
        if command_name in cmd.bot.modules.alts:
            command_name = cmd.bot.modules.alts[command_name]
        response = discord.Embed()
        if command_name not in cmd.bot.modules.commands.keys():
            response.colour = 0xBE1931
            response.title = f'❗ Command `{command_name}` was not found.'
        else:
            module_to_reload = cmd.bot.modules.commands[command_name].command
            reimport(module_to_reload)
            response.colour = 0x77B255
            response.title = f'✅ Command `{command_name}` was reloaded.'
        await message.channel.send(embed=response)
