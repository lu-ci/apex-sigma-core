import discord


async def unbindinvite(cmd, message, args):
    if message.author.guild_permissions.create_instant_invite:
        if args:
            invite_id = args[0]
            forced = args[-1] == ':f'
            invites = await message.guild.invites()
            target_inv = discord.utils.find(lambda inv: inv.id.lower() == invite_id.lower(), invites)
            if target_inv or forced:
                if forced:
                    inv_id = invite_id
                else:
                    inv_id = target_inv.id
                bindings = await cmd.db.get_guild_settings(message.guild.id, 'BoundInvites')
                if bindings is None:
                    bindings = {}
                if inv_id in bindings:
                    bindings.pop(inv_id)
                    await cmd.db.set_guild_settings(message.guild.id, 'BoundInvites', bindings)
                    title = f'✅ Invite {inv_id} has been unbound.'
                    response = discord.Embed(color=0x77B255, title=title)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invite {}.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ An invite with that ID was not found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments. Invite and role name needed.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Create Instant Invites needed.', color=0xBE1931)
    await message.channel.send(embed=response)
