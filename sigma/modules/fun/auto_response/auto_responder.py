import string

from sigma.core.utilities.data_processing import command_message_parser


def clean_word(text):
    output = ''
    for char in text:
        if char.lower() not in string.punctuation:
            output += char.lower()
    return output


async def auto_responder(ev, message):
    if message.guild:
        if message.content:
            pfx = ev.bot.get_prefix(message)
            if not message.content.startswith(pfx):
                triggers = ev.db.get_guild_settings(message.guild.id, 'ResponderTriggers')
                if triggers is None:
                    triggers = {}
                arguments = message.content.split(' ')
                for arg in arguments:
                    arg = clean_word(arg)
                    if arg in triggers:
                        response = triggers[arg]
                        response = command_message_parser(message, response)
                        await message.channel.send(response)
                        break
