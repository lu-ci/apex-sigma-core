import arrow
import discord


async def listwarnings(cmd, message, args):
    if message.author.guild_permissions.manage_messages:
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author
    else:
        target = message.author
    if target:
        lookup = {'guild': message.guild.id, 'target.id': target.id, 'warning.active': True}
        warnings = await cmd.db[cmd.db.db_cfg.database].Warnings.find(lookup).to_list(None)
        if warnings:
            warn_list = []
            for warning in warnings:
                warn_id = warning.get('warning').get('id')
                mod_id = warning.get('moderator').get('id')
                moderator = discord.utils.find(lambda x: x.id == mod_id, cmd.bot.get_all_members())
                if moderator:
                    moderator = moderator.name
                else:
                    moderator = warning.get('moderator').get('name')
                warn_time = arrow.get(warning.get('warning').get('timestamp')).format('DD. MMM. YYYY. HH:mm')
                warn_list.append(f'`{warn_id}` by **{moderator}** on {warn_time}.')
            warn_list = '\n'.join(warn_list)
            ending = 'warnings' if len(warnings) > 1 else 'warning'
            start = f'{target.name} has' if target.id != message.author.id else 'You have'
            response = discord.Embed(color=0xFFCC4D)
            response.add_field(name=f'⚠ {start} {len(warnings)} active {ending}.', value=warn_list)
        else:
            start = f'{target.name} doesn\'t' if target.id != message.author.id else 'You don\'t'
            response = discord.Embed(color=0x55acee, title=f'💠 {start} have any warnings.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ You didn\'t tag any user.')
    await message.channel.send(embed=response)
