import discord

from sigma.core.utilities.data_processing import user_avatar


async def quote(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = args[0]
        try:
            lookup = int(lookup)
        except ValueError:
            lookup = None
        if lookup:
            msg = None
            for channel in message.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    try:
                        msg = await channel.get_message(lookup)
                        break
                    except discord.Forbidden:
                        msg = None
                    except discord.NotFound:
                        msg = None
            if msg:
                if msg.content:
                    location = f'{msg.guild.name} | #{msg.channel.name}'
                    response = discord.Embed(color=msg.author.color, timestamp=msg.created_at)
                    response.set_author(name=f'{msg.author.display_name}', icon_url=user_avatar(msg.author))
                    response.description = msg.content
                    response.set_footer(text=location)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ That message has no text content.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Message not found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid ID given.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No ID given.')
    await message.channel.send(embed=response)
