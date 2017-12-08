import discord

from .nodes.permission_data import get_all_perms


async def enablemodule(cmd, message, args):
    if args:
        if not message.author.permissions_in(message.channel).manage_guild:
            response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
        else:
            mdl_name = args[0].lower()
            if mdl_name in cmd.bot.modules.categories:
                perms = await get_all_perms(cmd.db, message)
                disabled_modules = perms['DisabledModules']
                if mdl_name in disabled_modules:
                    disabled_modules.remove(mdl_name)
                    perms.update({'DisabledModules': disabled_modules})
                    await cmd.db[cmd.db.db_cfg.database].Permissions.update_one({'ServerID': message.guild.id},
                                                                                {'$set': perms})
                    response = discord.Embed(color=0x77B255, title=f'✅ `{mdl_name.upper()}` enabled.')
                else:
                    response = discord.Embed(color=0xFFCC4D, title='⚠ Module Not Disabled')
            else:
                response = discord.Embed(color=0x696969, title='🔍 Module Not Found')
        await message.channel.send(embed=response)
