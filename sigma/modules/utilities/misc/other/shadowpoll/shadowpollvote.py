import discord

from sigma.core.mechanics.command import SigmaCommand


def origin(x, poll_file):
    return x.id == poll_file["origin"]["server"]


def check_roles(allowed_roles, all_users, user):
    members = []
    for member in all_users:
        if isinstance(member, discord.Member):
            if member.id == user.id:
                members.append(member)
    authorized = False
    for member_item in members:
        for allowed_role in allowed_roles:
            role = discord.utils.find(lambda x: x.id == allowed_role, member_item.roles)
            if role:
                authorized = True
                break
        if authorized:
            break
    return authorized


async def shadowpollvote(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) == 2:
            poll_id = args[0].lower()
            try:
                choice_num = int(args[1])
            except ValueError:
                choice_num = None
            if choice_num:
                poll_file = await cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    choice_count = len(poll_file['poll']['answers'])
                    if 0 > choice_num > choice_count:
                        bad_choice = True
                    else:
                        bad_choice = False
                    if not bad_choice:
                        active = poll_file['settings']['active']
                        if active:
                            perms = poll_file['permissions']
                            chn_p = perms['channels']
                            rol_p = perms['roles']
                            usr_p = perms['users']
                            if not chn_p and not rol_p and not usr_p:
                                authorized = True
                            else:
                                rol_auth = check_roles(rol_p, cmd.bot.get_all_members(), message.author)
                                if message.channel:
                                    chn_auth = message.channel.id in chn_p
                                else:
                                    chn_auth = False
                                usr_auth = message.author.id in usr_p
                                if rol_auth or usr_auth or chn_auth:
                                    authorized = True
                                else:
                                    authorized = False
                            if authorized:
                                if str(message.author.id) in poll_file['votes']:
                                    ender = 'updated'
                                else:
                                    ender = 'recorded'
                                poll_file['votes'].update({str(message.author.id): choice_num})
                                poll_coll = cmd.db[cmd.db.db_cfg.database].ShadowPolls
                                await poll_coll.update_one({'id': poll_id}, {'$set': poll_file})
                                response = discord.Embed(color=0x66CC66, title=f'✅ Your choice has been {ender}.')
                            else:
                                response = discord.Embed(color=0xFFCC4D, title='🔒 Not authorized to vote.')
                        else:
                            response = discord.Embed(color=0xFFCC4D, title='🔒 That poll is not active.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Choice number out of range.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not a valid choice number.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing the choice number.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID and choice.')
    await message.channel.send(embed=response)
