import datetime

import arrow
import discord


class StatsConstructor(object):
    @staticmethod
    def gen_time_data(time: datetime.datetime):
        arw = arrow.get(time)
        time_data = {
            '@timestamp': arw.format("YYYY-MM-DDTHH:mm:ssZ"),
            'timestamp': {
                'integer': arw.timestamp,
                'float': arw.float_timestamp
            }
        }
        return time_data

    @staticmethod
    def gen_cmd_data(c):
        command_data = {
            'name': c.name,
            'path': c.path,
            'category': c.category,
            'nsfw': c.nsfw,
            'owner': c.owner,
            'dmable': c.dmable,
            'requirements': c.requirements
        }
        return command_data

    def gen_chn_data(self, c: discord.TextChannel):
        channel_data = {
            'id': str(c.id),
            'name': c.name,
            'nsfw': c.is_nsfw(),
            'members': len(c.members),
            'created': self.gen_time_data(c.created_at),
            'category': c.category.name if c.category else None
        }
        return channel_data

    def gen_gld_data(self, g: discord.Guild):
        total = 0
        bots = {'online': 0, 'idle': 0, 'dnd': 0, 'offline': 0, 'total': 0}
        users = {'online': 0, 'idle': 0, 'dnd': 0, 'offline': 0, 'total': 0}
        for member in g.members:
            total += 1
            if member.bot:
                target_dict = bots
            else:
                target_dict = users
            target_total = target_dict.get('total') + 1
            target_dict.update({'total': target_total})
            status_total = target_dict.get(member.status.name) + 1
            target_dict.update({member.status.name: status_total})
        category_count = 0
        text_channel_count = 0
        voice_channel_count = 0
        for channel in g.channels:
            if isinstance(channel, discord.CategoryChannel):
                category_count += 1
            elif isinstance(channel, discord.TextChannel):
                text_channel_count += 1
            elif isinstance(channel, discord.VoiceChannel):
                voice_channel_count += 1
        guild_data = {
            'id': str(g.id),
            'name': g.name,
            'large': g.large,
            'channels': {
                'text': text_channel_count,
                'voice': voice_channel_count,
                'system': self.gen_chn_data(g.system_channel) if g.system_channel else None,
                'categories': category_count
            },
            'members': {
                'total': total,
                'bots': bots,
                'users': users
            },
            'owner': self.gen_usr_data(g.owner),
            'region': str(g.region),
            'mfa': g.mfa_level,
            'verification': g.verification_level
        }
        return guild_data

    def gen_usr_data(self, u: discord.Member):
        member_data = {
            'id': str(u.id),
            'name': {
                'username': u.name,
                'nickname': u.nick,
                'displayname': u.display_name
            },
            'times': {
                'joined': self.gen_time_data(u.joined_at),
                'created': self.gen_time_data(u.created_at)
            },
            'activity': {
                'name': u.activity.name if u.activity else None,
                'type': u.activity.type if u.activity else None
            },
            'status': u.status.value,
            'owner': u.id == u.guild.owner.id,
            'role': self.gen_rol_data(u.top_role),
            'nitro': u.is_avatar_animated()
        }
        return member_data

    def gen_rol_data(self, r: discord.Role):
        role_data = {
            'id': str(r.id),
            'name': r.name,
            'created': self.gen_time_data(r.created_at),
            'members': len(r.members),
            'hoist': r.hoist,
            'color': r.color.value,
            'mentionable': r.mentionable
        }
        return role_data

    def gen_msg_data(self, m: discord.Message):
        message_data = {
            'id': str(m.id),
            'guild': self.gen_gld_data(m.guild),
            'author': self.gen_usr_data(m.author),
            'channel': self.gen_chn_data(m.channel)
        }
        return message_data

    def construct_cmd_data(self, cmd, msg: discord.Message, args: list):
        entry_data = {
            'command': self.gen_cmd_data(cmd),
            'message': self.gen_msg_data(msg),
            'arguments': {
                'full': ' '.join(args),
                'items': args
            },
            'time': self.gen_time_data(arrow.utcnow().datetime)
        }
        return entry_data
