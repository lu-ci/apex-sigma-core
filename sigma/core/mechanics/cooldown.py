import arrow


class CooldownControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db
        self.cds = self.db[self.bot.cfg.db.database].CooldownSystem

    def on_cooldown(self, cmd, user):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cds.find_one({'name': cd_name})
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

    def get_cooldown(self, cmd, user):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cds.find_one({'name': cd_name})
        if entry:
            end_stamp = entry['end_stamp']
            now_stamp = arrow.utcnow().float_timestamp
            cooldown = end_stamp - now_stamp
            if cooldown < 2:
                cooldown = round(cooldown, 2)
        else:
            cooldown = 0
        return cooldown

    def set_cooldown(self, cmd, user, amount):
        if isinstance(user, str):
            cd_name = f'cd_{cmd}_{user}'
        else:
            cd_name = f'cd_{cmd}_{user.id}'
        entry = self.cds.find_one({'name': cd_name})
        end_stamp = arrow.utcnow().timestamp + amount
        if entry:
            self.cds.update_one({'name': cd_name}, {'$set': {'end_stamp': end_stamp}})
        else:
            cd_data = {
                'name': cd_name,
                'end_stamp': end_stamp
            }
            self.cds.insert_one(cd_data)
