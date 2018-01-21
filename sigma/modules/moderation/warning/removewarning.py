import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import permission_denied


def make_log_embed(author: discord.Member, target: discord.Member, warn_data: dict):
    target_avatar = user_avatar(target)
    author_descrp = f'{author.mention}\n{author.name}#{author.discriminator}'
    target_descrp = f'{target.mention}\n{target.name}#{target.discriminator}'
    response = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
    response.set_author(name=f'{target.name} has been un-warned by {author.name}.', icon_url=target_avatar)
    response.add_field(name='⚠ Warned User', value=target_descrp, inline=True)
    response.add_field(name='🛡 Moderator', value=author_descrp, inline=True)
    response.set_footer(text=f'[{warn_data.get("warning").get("id")}] UserID: {target.id}')


async def removewarning(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_messages:
        if message.mentions:
            if len(args) == 2:
                target = message.mentions[0]
                warn_id = args[1].lower()
                warn_id = args[1].lower()
                lookup = {
                    'guild': message.guild.id,
                    'target.id': target.id,
                    'warning.id': warn_id,
                    'warning.active': True
                }
                warn_data = await cmd.db[cmd.db.db_cfg.database].Warnings.find_one(lookup)
                if warn_data:
                    warn_iden = warn_data.get('warning').get('id')
                    change_data = {'$set': {'warning.active': False}}
                    await cmd.db[cmd.db.db_cfg.database].Warnings.update_one(lookup, change_data)
                    response = discord.Embed(color=0x77B255, title=f'✅ Warning {warn_iden} deactivated.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 {target.name} has no {warn_id} warning.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ Both user tag and warning ID are needed.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ You didn\'t tag any user.')
    else:
        response = permission_denied('Manage Messages')
    await message.channel.send(embed=response)
