import arrow


class CommandCooldown(object):
    def __init__(self):
        self.cooldowns = {}
        self.interval = 1.35

    def get_cooldown(self, ident):
        cd_data = self.cooldowns.get(ident) or 0
        now = arrow.utcnow().float_timestamp
        cd = cd_data - now
        return cd

    def set_cooldown(self, ident):
        now = arrow.utcnow().float_timestamp
        new_stamp = now + self.interval
        self.cooldowns.update({ident: new_stamp})

    def on_cooldown(self, ident):
        cd_data = self.cooldowns.get(ident) or 0
        now = arrow.utcnow().float_timestamp
        if cd_data > now:
            on_cd = True
        else:
            on_cd = False
        return on_cd


class CooldownControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.cmd = CommandCooldown()
        self.db = self.bot.db
        self.cds = self.db[self.bot.cfg.db.database].CooldownSystem

    async def on_cooldown(self, cmd, user):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = await self.cds.find_one({'name': cd_name})
        if entry:
            end_stamp = entry['end_stamp']
            now_stamp = arrow.utcnow().timestamp
            if now_stamp > end_stamp:
                cooldown = False
            else:
                cooldown = True
        else:
            cooldown = False
        return cooldown

    async def get_cooldown(self, cmd, user):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = await self.cds.find_one({'name': cd_name})
        if entry:
            end_stamp = entry['end_stamp']
            now_stamp = arrow.utcnow().float_timestamp
            cooldown = end_stamp - now_stamp
            if cooldown < 2:
                if cooldown <= 0:
                    cooldown = 0.01
                else:
                    cooldown = round(cooldown, 2)
            else:
                cooldown = int(cooldown)
        else:
            cooldown = 0
        return cooldown

    async def set_cooldown(self, cmd, user, amount):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = await self.cds.find_one({'name': cd_name})
        end_stamp = arrow.utcnow().timestamp + amount
        if entry:
            await self.cds.update_one({'name': cd_name}, {'$set': {'end_stamp': end_stamp}})
        else:
            cd_data = {
                'name': cd_name,
                'end_stamp': end_stamp
            }
            await self.cds.insert_one(cd_data)
