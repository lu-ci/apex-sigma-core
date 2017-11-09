from sigma.core.mechanics.permissions import GlobalCommandPermissions
from sigma.core.utilities.data_processing import command_message_parser


def log_command_usage(log, message, command):
    if message.guild:
        cmd_location = f'SRV: {message.guild.name} [{message.guild.id}] | '
        cmd_location += f'CHN: #{message.channel.name} [{message.channel.id}]'
    else:
        cmd_location = 'DIRECT MESSAGE'
    author_full = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
    log_text = f'USR: {author_full} | {cmd_location} | CMD: {command}'
    log.info(log_text)


async def custom_command(ev, message):
    if message.guild:
        prefix = ev.bot.get_prefix(message)
        if message.content.startswith(prefix):
            if message.content != prefix:
                cmd = message.content[len(prefix):].lower().split()[0]
                if cmd not in ev.bot.modules.commands:
                    perms = GlobalCommandPermissions(ev, message)
                    if perms.permitted:
                        custom_commands = ev.db.get_guild_settings(message.guild.id, 'CustomCommands')
                        if custom_commands is None:
                            custom_commands = {}
                        if cmd in custom_commands:
                            cmd_text = custom_commands[cmd]
                            response = command_message_parser(message, cmd_text)
                            log_command_usage(ev.log, message, cmd)
                            await message.channel.send(response)
